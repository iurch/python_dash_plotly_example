
def covid_ts(pd,URL):
    _covid_ts= pd.read_csv(URL)
    return _covid_ts
    #return 'Not any more COVID-19'

#get data in cleaned time series format for country
#Return data frame
def process_data(pd,data,cntry='US',window=3):
    conf_ts= data
    conf_ts_cntry= conf_ts[conf_ts['Country/Region']==cntry]
    final_dataset= conf_ts_cntry.T[4:].sum(axis='columns').diff().rolling(window=window).mean()[40:]
    df= pd.DataFrame(final_dataset,columns=['Total'])
    return df

#get overall wordlwide total for confirmed, recovered and dead cases
def get_overall_total(df):
    return df.iloc[:,-1].sum()

#get total for confirmed, recovered and dead for country
def get_cntry_total(df,cntry='US'):
    return df[df['Country/Region']==cntry].iloc[:, -1].sum()

