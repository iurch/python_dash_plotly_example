# @imports
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash.dependencies import Input, Output

# @setting
pd.set_option('max_rows',20)
pio.renderers.default = 'browser'

# @Constants
from modules.constantes import CONF_URL, DEAD_URL, RECV_URL
import readfile as f

# @Custom Graphics
import custom_plotly as cplot

# @MAIN
def main():
    covid_conf_ts = f.covid_ts(pd,CONF_URL)
    covid_dead_ts = f.covid_ts(pd,DEAD_URL)
    #covid_recv_ts = f.covid_ts(pd,RECV_URL)  # Just contain one row

    _df_conf= f.process_data(pd,covid_conf_ts)
    conf_overall_total= f.get_overall_total(_df_conf)
    
    _df_dead= f.process_data(pd,covid_dead_ts)
    dead_overall_total= f.get_overall_total(_df_dead)
    
    #_df_recv= f.process_data(pd,covid_recv_ts)
    #recv_overall_total= f.get_overall_total(_df_recv)

    print('Overall Confirmed: ', conf_overall_total)
    print('Overall Dead: ', dead_overall_total)
    #print('Overall Recovered: ' , recv_overall_total)

    cntry= 'US'
    cnf_cntry_total= f.get_cntry_total(covid_conf_ts, cntry)
    dead_cntry_total= f.get_cntry_total(covid_dead_ts, cntry)
    #recovered_cntry_total= f.get_cntry_total(covid_recv_ts,cntry)

    print(f'{cntry} Confirmed: ', cnf_cntry_total)
    print(f'{cntry} Dead: ', dead_cntry_total)
    #print(f'{cntry} Recovered: ', recovered_cntry_total)


    # plotly GENERATE Line Graph using Plotly
    #fig= cplot.fig_world_trend(pd,px,covid_conf_ts,cntry,1) # Is used by graph1() function

    # @DASH APP
    external_stylesheets= [dbc.themes.BOOTSTRAP]
    app= dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.title= 'Covid-19 Dashboard'

    # @Page Header
    colors= {
        'background': '#111111',
        'bodyColor': '#F2DFCE',
        'text': '#7FDBFF'
    }

    def get_page_heading_style():
        return {'backgroundcolor': colors['background']}


    def get_page_heading_title():
        return html.H1(children='COVID-19 Dashboard',style={'textAlign':'center','colors': colors['text']})

    def get_page_heading_subtitle():
        return html.Div(children='visualize Covid-19 data generated from sources all over the world.', style={'textAlign':'center','color':colors['text']})

    def generate_page_header():
        main_header= dbc.Row([dbc.Col(get_page_heading_title(),md=12)],align='center',style=get_page_heading_style())
        subtitle_header= dbc.Row([dbc.Col(get_page_heading_subtitle(),md=12)],align='center',style= get_page_heading_style())
        header= (main_header,subtitle_header)
        return header

    # @Select Country Dropdown
    def get_country_list():
        return covid_conf_ts['Country/Region'].unique()

    def create_dropdown_list(cntry_list):
        dropdown_list= []
        for cntry in sorted(cntry_list):
            tmp_dict= {'label':cntry, 'value':cntry}
            dropdown_list.append(tmp_dict)
        return dropdown_list

    def get_country_dropdown(id):
        return html.Div([html.Label('Select Country'), dcc.Dropdown(id='my-id' + str(id),options= create_dropdown_list(get_country_list()),value='US'), html.Div(id='my-div'+str(id))])

    # @Graph container for DASH
    def graph1():
        return dcc.Graph(id='graph1', figure= cplot.fig_world_trend(pd,px,covid_conf_ts,'US',1))

    # @Generate CARDS for overall numbers
    def generate_card_content(card_header,card_value,overall_value):
        card_head_style= {'textAlign':'center','fontSize':'150%'}
        card_body_style= {'textAlign':'center','fontSize':'200%'}
        card_header= dbc.CardHeader(card_header,style= card_head_style)
        card_body= dbc.CardBody([html.H5(f'{int(card_value):,}',className='card_title',style=card_body_style),html.P("worldwide: {:,}".format(overall_value),className='card_text',style= {'textAlign':'center'}),])
        card= [card_header,card_body]
        return card
    
    def generate_cards(cntry='US'):
        cards= html.Div([dbc.Row([dbc.Col(dbc.Card(generate_card_content('Confirmed',cnf_cntry_total,conf_overall_total),color='warning',inverse=True),md=dict(size=2,offset=3)),dbc.Col(dbc.Card(generate_card_content('Dead',dead_cntry_total,dead_overall_total),color='dark',inverse=True),md=dict(size=2)),],className='mb-4',)], id='card1')
        return cards

    # @DASH Slider for Moving Average Window
    def get_slider():
        return html.Div([dcc.Slider(id='my-slider',min=1,max=15,step=None,marks={1:'1',3:'3',5:'5',7:'1-week',14:'Fortnight'},value=3,),html.Div([html.Label('Select Moving Average Window')],id='my-div'+str(id),style={'textAlign':'center'})])
    
    # @Generate APP layout
    def generate_layout():
        page_header= generate_page_header()
        layout= dbc.Container([page_header[0],page_header[1],html.Hr(),generate_cards(),html.Hr(),dbc.Row([dbc.Col(get_country_dropdown(id=1),md=dict(size=4, offset=4))]),dbc.Row([dbc.Col(graph1(),md=dict(size=6, offset=3))],align='center',),dbc.Row([dbc.Col(get_slider(),md=dict(size=4,offset=4))]),],fluid=True,style={'backgroundColor':colors['bodyColor']})
        return layout

    app.layout = generate_layout()

    # @Assign DASH Callbacks
    @app.callback([Output(component_id='graph1', component_property='figure'),Output(component_id='card1',component_property='children')],[Input(component_id='my-id1',component_property='value'),Input(component_id='my-slider',component_property='value')])

    def update_output_div(input_value1, input_value2):
        return cplot.fig_world_trend(pd,px,covid_conf_ts,input_value1,input_value2),generate_cards(input_value1)

    # @Run Server
    app.run_server(host='0.0.0.0', debug= False)


# @Validation
if __name__ == "__main__":
    main()