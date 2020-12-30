

#Generate Line Graph using Plotly

def fig_world_trend(pd,px,data,cntry='US',window=3):
    from readfile import process_data
    
    df= process_data(pd,data,cntry=cntry,window=window)
    df.head(10)
    if window== 1:
        yaxis_title= 'Daily Cases'
    else:
        yaxis_title= 'Daily Cesas ({}-day MA)'.format(window)
    fig= px.line(df, y='Total', x=df.index, title='Daily confirmed cases trend for {}'.format(cntry),height=600, color_discrete_sequence= ['maroon'])
    fig.update_layout(title_x=0.5, plot_bgcolor='#F2DFCE',paper_bgcolor='#F2DFCE',xaxis_title='Date',yaxis_title=yaxis_title)
    return fig