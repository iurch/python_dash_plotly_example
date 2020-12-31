
#Generate Line Graph using Plotly
def fig_world_trend(pd,px,data,op='miliseconds'):
    from readfile import process_data
    
    df= process_data(pd,data,op=op)
    #df.head(10) # the first 10 rows
    #print(df)
    #print(df.index)
    fig= px.line(df, y=op, x=df.index, title='{}'.format(op),height=600, color_discrete_sequence= ['green'])
    fig.update_layout(title_x=0.5, plot_bgcolor='#99b3ff',paper_bgcolor='#99b3ff',xaxis_title='time',yaxis_title=op)
    return fig