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
from modules.constantes import DATA_CSV,CONF_URL, DEAD_URL, RECV_URL
import readfile as f

# @Custom Graphics
import custom_plotly as cplot

# @MAIN
def main():
    print(5 * '*' , 'PANDAS VERSION ',pd.__version__, 5 * '*')

    data_ts= f.read_file_csv(pd,URL=DATA_CSV,header=['bytes','med','from','ip','icmp','ttl','time','medida'])
    data_ts= data_ts.dropna() # Delete the row with NaN

    data_ts['miliseconds']= pd.to_numeric(data_ts['time'].map(lambda x: x.lstrip('time=').rstrip(' ')),downcast='float')
    mean= data_ts['miliseconds'].mean()

    print('MEAN ',mean)
    print('MAX [ms]',data_ts['miliseconds'].max())
    print('MAX [idx] ',data_ts['miliseconds'].idxmax())

    
    # @DASH APP
    external_stylesheets= [dbc.themes.BOOTSTRAP]
    app= dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.title= 'Time for PING Google'

    # @Page Header
    colors= {'background': '#111111','bodyColor': '#5dbcd2','text': '#7FDBFF'}

    def get_page_heading_style():
        return {'backgroundcolor': colors['background']}

    def get_page_heading_title():
        return html.H1(children='PING GOOGLE SERVER',style={'textAlign':'center','colors': colors['text']})

    def get_page_heading_subtitle():
        return html.Div(children='visualize PING data generated from sources all.', style={'textAlign':'center','color':colors['text']})

    def generate_page_header():
        main_header= dbc.Row([dbc.Col(get_page_heading_title(),md=12)],align='center',style=get_page_heading_style())
        subtitle_header= dbc.Row([dbc.Col(get_page_heading_subtitle(),md=12)],align='center',style= get_page_heading_style())
        header= (main_header,subtitle_header)
        return header

    # @Graph container for DASH
    def graph1():
        return dcc.Graph(id='graph1', figure= cplot.fig_world_trend(pd,px,data=data_ts,op='miliseconds'))

    # @Generate CARDS for overall numbers
    def generate_card_content(card_header,card_value):
        card_head_style= {'textAlign':'center','fontSize':'150%'}
        card_body_style= {'textAlign':'center','fontSize':'200%'}
        card_header= dbc.CardHeader(card_header,style= card_head_style)
        card_body= dbc.CardBody([html.H5(f'{round(float(card_value),2):,} ms',className='card_title',style=card_body_style),])
        card= [card_header,card_body]
        return card
    
    def generate_cards():
        cards= html.Div([dbc.Row([dbc.Col(dbc.Card(generate_card_content('Rate media ',mean),color='success',inverse=True),md=dict(size=2,offset=5)),],className='mb-6',)], id='card1')
        return cards

    # @Generate APP layout
    def generate_layout():
        page_header= generate_page_header()
        layout= dbc.Container([page_header[0],page_header[1],html.Hr(),generate_cards(),html.Hr(),dbc.Row([dbc.Col(graph1(),md=dict(size=6, offset=3))],align='center',),],fluid=True,style={'backgroundColor':colors['bodyColor']})
        return layout

    app.layout = generate_layout()

    # @Assign DASH Callbacks
    #@app.callback([Output(component_id='graph1', component_property='figure'),Output(component_id='card1',component_property='children')],[Input(component_id='my-id1',component_property='value'),Input(component_id='my-slider',component_property='value')])

    #def update_output_div(input_value1, input_value2):
    #    return cplot.fig_world_trend(pd,px,data_ts,input_value1,input_value2),generate_cards(input_value1)

    # @Run Server
    app.run_server(host='0.0.0.0', debug= False)


# @Validation
if __name__ == "__main__":
    main()