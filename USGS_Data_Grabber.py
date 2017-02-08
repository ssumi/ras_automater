
# coding: utf-8

# # Step-by-step guide to retrieving data from USGS API
# 
# ## Example: 
# ### Get streamflow data from selected gage for time period of interest & plot timeseries results


# Import libraries

import pandas as pd
import os
import requests
import json
from datetime import datetime
from collections import OrderedDict
import math


def WriteUnsteady(usgs_data,fout):      
    data_length = len(usgs_data)/10    
    nrows = math.ceil(data_length)
    
    j=0
    for i in range(nrows):
        #print('row ',i)
        row_values = usgs_data[j:j+10]
        output = str(row_values).strip('[]').replace(',', '')
        fout.write('    {}\n'.format(output))
        j = j+10    

def GrabData(gage, y0, m0 ,d0, y1, m1 ,d1,parameter):
                                    # Parameter 
    if parameter == '00060':
        obser     = "StreamFlow"
    else:
        obser     = "Stage"                                 # Observed data Requested
    dformat    = "json"                                  # Data Format  
    url        = 'http://waterservices.usgs.gov/nwis/iv' # USGS API
    

    
    # Create Datetime Objects
    start     = datetime(y0, m0, d0,0)    
    stop      = datetime(y1, m1 ,d1,0)         
    
    # Format Datetime Objects for USGS API
    first    =  datetime.date(start).strftime('%Y-%m-%d')
    last     =  datetime.date(stop).strftime('%Y-%m-%d') 
    

    
    # Ping the USGS API for data
    
    params = OrderedDict([('format',dformat),('sites',gage),('startDT',first), 
            ('endDT',last), ('parameterCD',parameter)])  
    r = requests.get(url, params = params) 
    print("Retrieved Data for USGS Gage: ", gage)
    data = r.content.decode()
    d = json.loads(data)
    

    
    # After reveiwing the JSON Data structure, select only data we need: 
    tseries = d['value']['timeSeries'][0]['values'][0]['value'][:]
    
  
    
    # Let's see what the keys are in the JSON output:
    mydict = dict(d['value']['timeSeries'][0])
    for key in mydict: print(key)
    
    
    # Great, We can pull the station name, and assign to a variable for use later:
    SiteName = mydict['sourceInfo']['siteName']
    print(SiteName)
    
  
    
    # Create a Dataframe, format Datetime data,and assign numeric type to observations
    df = pd.DataFrame.from_dict(tseries)
    df.index = pd.to_datetime(df['dateTime'],format='%Y-%m-%d{}%H:%M:%S'.format('T'))
    
    df['UTC Offset'] = df['dateTime'].apply(lambda x: x.split('-')[3][1])
    df['UTC Offset'] = df['UTC Offset'].apply(lambda x: pd.to_timedelta('{} hours'.format(x)))
    
    df.index = df.index - df['UTC Offset']
    df.value = pd.to_numeric(df.value)
    

    
    # Get Rid of unwanted data, rename observed data
    df = df.drop('dateTime', 1)
    df.drop('qualifiers',axis = 1, inplace = True)
    df.drop('UTC Offset',axis = 1, inplace = True)
    df = df.rename(columns = {'value':obser})
    
    #df.head()
    return df


