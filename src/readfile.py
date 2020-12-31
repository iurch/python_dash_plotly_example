#imports
import os

# read the file for pd and return ds
def read_file_csv(pd,URL,header):
    _ds= pd.read_csv(os.path.join(os.path.dirname(__file__),URL),skiprows=[0],error_bad_lines=False,header=None,delim_whitespace=True,names=header)
    return _ds

#get data in cleaned time series format for op
#Return data frame
def process_data(pd,data,op='miliseconds'):
    conf_ts= data[op].copy()
    df= pd.DataFrame(conf_ts,columns=[op])
    return df