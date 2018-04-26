# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:53:27 2017

@author: seth/arslaan
"""

#-----------------------------------------------------------------

#---Import Libraries
import os
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime, timezone,timedelta

##---get the data from NOAA

def NOAA_forecast(gage):
    
    #---Example ahps stations:
    
    bld='BLDM2'
    lwt='LWTV2'
    ncd='NCDV2'
    alex = 'AXTV2'    
    cbbt = 'CBBV2'
    wadc ='WASD2'
    gtwn ='GTND2'
    l_falls = 'BRKM2'
    mach_ck = 'NCDV2'
    anapolis = 'APAM2'
    
    #gage = lwt
    
    #---Read HTML
    
    #url = r'http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage={}&output=tabular'.format(gage)                 # UTC timezone data link
    
    url = r'http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage={}&output=tabular&time_zone=est'.format(gage) # EST timezone data link
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    
    #---Data
    data = soup.find_all('table')[0] 
    data_rows = data.find_all('tr')[3:]
    
    
    #--Get the Current Year 
    year = datetime.now().strftime("%Y")
    
    #--Initialize Dictionaries
    obs_data =  {'Date(EST)' : [], 'Flow' : [], 'Stage' : []}
    forecast_data = {'Date(EST)' : [], 'Flow' : [], 'Stage' : []}
    
    #---Extract Values to Dictionaries
    value = 'Observed'
    
    
    for row in data_rows:
        d = row.find_all('td')
        try:
            dtm   = d[0].get_text().split()[0] + '/' + str(year) +' '+ d[0].get_text().split()[1]
            stage = d[1].get_text()
            flow  = d[2].get_text()
        
            if value == 'Observed':
                obs_data['Date(EST)'].append(dtm) 
                obs_data['Flow'].append(flow)
                obs_data['Stage'].append(stage)
    
            elif value =='Forecast':
                forecast_data['Date(EST)'].append(dtm) 
                forecast_data['Flow'].append(flow)
                forecast_data['Stage'].append(stage)
    
        except:
            check_value = str(d)
            if 'Forecast  Data ' in check_value:
                value = 'Forecast'
            
    #---Create & Format Dataframes
    df_obs = pd.DataFrame.from_dict(obs_data)
    df_obs['Date(EST)'] = pd.to_datetime(df_obs['Date(EST)'], format='%m/%d/%Y %H:%M')
    df_obs['Stage'] = df_obs['Stage'].astype(str).str[:-2].astype(np.float)
    #df_obs = df_obs.set_index(df_obs['Date(EST)'] )
    
    #########################################################
    #--Reverse rows to get from previous to current date
    #########################################################
    df_obs = df_obs.iloc[::-1]
  
    df_fcst = pd.DataFrame.from_dict(forecast_data)   
    df_fcst['Date(EST)'] = pd.to_datetime(df_fcst['Date(EST)'], format='%m/%d/%Y %H:%M')
    df_fcst['Stage'] = df_fcst['Stage'].astype(str).str[:-2].astype(np.float)
    #df_fcst = df_fcst.set_index(df_fcst['Date(EST)'] )
    
    #start, stop = df_obs.index[0], df_fcst.index[-1]
    #idx = pd.date_range(start,stop,freq='15T')           
                
                
    #--Initialize Plots
    fig, ax = plt.subplots(figsize=(12,6))
    
    #--Plot Observed
    x0 = df_obs['Date(EST)']
    y0 = df_obs['Stage']
    ax.plot(x0 ,y0, color = 'b')       # Observed
    
    
    #--Plot Forecast
    x1 = df_fcst['Date(EST)']
    y1 = df_fcst['Stage']
    ax.plot(x1 ,y1, color = 'r')       # Observed
    
    #ax.scatter(x,y1,color='b', marker = 'o', s= 55, facecolors='none')      # Forecast
    
    
    plt.legend(['Observed', 'Forecast'], loc='lower left',scatterpoints = 1)
    ax.plot(x0 ,y0, color = 'b', marker = 'o')       # Add Points
    ax.plot(x1 ,y1, color = 'r', marker = 'o')       # Add Points
    
    plt.title('AHPS Data: {}'.format(gage))
    plt.xlabel('(EST)')
    plt.ylabel('Stage (ft)')
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%b %d %H:%M'))
    plt.gca().xaxis.set_major_locator(HourLocator(np.arange(0, 25, 12)))
    
    plt.gcf().autofmt_xdate()  
    plt.close()
#    
#    obs_end_date = df_fcst['Date(EST)'].iloc[0] - timedelta(hours=6)
#    obs_end = obs_end_date.strftime(format = '%Y-%m-%d %H:%M:%S')
#    
#    obs_start_date = obs_end_date - timedelta(2) 
#    obs_start = obs_start_date.strftime(format = '%Y-%m-%d %H:%M:%S')
#    
#    idx2 = pd.date_range(obs_start,obs_end ,freq='6H')
#    obs_fcst_add = df_obs.append(df_fcst)
      
   
#    obs_fcst_add.index = obs_fcst_add['Date(EST)']
#    obs_fcst_add = obs_fcst_add.reindex(idx2, fill_value = '')
       
    return df_fcst
    #return obs_fcst_add       
            