
# -*- coding: utf-8 -*-

"""
Created on Tue May 16 11:48:09 2017

@author: 

"""

import matplotlib.pyplot as plt
import fileinput
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests
from scipy.interpolate import interp1d
import csv
import numpy as np


def NOAA_TIDES(tide_gage,start,noaa_idx,freq):
    
    #--Datetime for data download
    #start, freq = "03-2017-01 00:00","3600s" #---Date Format: %m-%Y-%d %H:%M
    #noaa_idx =  pd.date_range('03/01/2017 00:00:00','04/01/2017 00:00:00',freq='H')
    
    
    #-- Stations and data
    #tide_gage = '8635750' # Lewisetta
    
    nodesx = {'1':{tide_gage:[]}}   
    # nodesx = {'1':{'8594900':[]}}
    noaa_time_step = '6T'
    
    #--NOAA API https://tidesandcurrents.noaa.gov/api/
    datum     = "NAVD"   #"NAVD"                #Datum
    units     = "metric"                        #Units
    time_zone = "gmt"                           #Time Zone
    fmt       = "json"                          #Format
    url       = 'http://tidesandcurrents.noaa.gov/api/datagetter'
    product   = 'water_level'                   #Product
    
    
    #--------- Add duration of data set in hours
    
    period = len(noaa_idx)
    
    # creating data set
    l =[]        
    l.extend(range(1, period+1))
      
          
    #---------------------Ping NOAA API for Validation Data,Create NOAA Dataframe
    
    noaa = pd.DataFrame()
    gages = dict()
    
    first = datetime.datetime.strptime(start,"%m-%Y-%d %H:%M")
    last =  pd.date_range(first,periods = period, freq=freq)[-1]
     
    for n in nodesx:
        for key in nodesx[n]:
            g = int(key)
           
        t0 = first.strftime('%Y%m%d %H:%M')
        t1 = last.strftime('%Y%m%d %H:%M')
        api_params = {'begin_date': t0, 'end_date': t1,
                    'station': g,'product':product,'datum':datum,
                    'units':units,'time_zone':time_zone,'format':fmt,
                    'application':'web_services' }
            
        pred=[];obsv=[];t=[]
    
        try:
            r = requests.get(url, params = api_params)
            jdata =r.json()
        
            for j in jdata['data']:
                t.append(str(j['t']))
                obsv.append(str(j['v']))
                pred.append(str(j['s']))
            colname = str(g)    
            noaa[colname]= obsv
            noaa[colname] = noaa[colname].astype(float)
            gages[jdata['metadata']['id']]=jdata['metadata']['name']
        except:
            print(g,'No Data')  
         
    idx = pd.date_range(first,periods = len(noaa.index), freq=noaa_time_step)   
    noaa = noaa.set_index(idx)   
    df = pd.DataFrame(l)
    df = df.set_index(noaa_idx)
    df = df.merge(noaa,left_index=True, right_index=True)
    df.drop([0],axis=1,inplace=True)
    
    # first data set
    df_store = pd.DataFrame(df) 
    #return df  ##  1 HOUR
    
    ## PLOT
    if tide_gage == "8635750":
        gage_name = "Lewisetta"
    elif tide_gage == "8635027":
        gage_name = "Dahlgren"
    elif tide_gage == "8594900":
        gage_name = "Washington DC"
        
    noaa.plot(grid = True,figsize=(10,5), title = '{} (Stage in meter)'.format(gage_name))
    #os.chdir('C:\\Users\\admin\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    plt.savefig('{}.PNG'.format(gage_name))
    plt.close()
    return noaa ## 6 MIN
  
  
#os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
#with open('PeakStagesNOAA_{}.csv'.format(g),'w') as f:
#   df_final1.to_csv(f, index=True,header = True)
#    
# 
#
## merging dataframes 
#
#bla = [df_final , df]
#df_final1 = pd.concat(bla)
#df_final1 = df_final1.sort_index(axis=0, level=None, ascending=True)
#df_final1.plot()    
#df_store = df_store.merge(df,left_index=True, right_index=True)
