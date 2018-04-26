# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:53:27 2017

@author: seth/arslaan
"""

#---Import Libraries
import os
import math
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime, timezone,timedelta

##---get the data from NOAA
def NOAA_forecast_obs_no_flow(gage):
    
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
    piney = 'SGSM2'
    
    #gage =piney
    
    #---Read HTML
    #url = r'http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage={}&output=tabular'.format(gage)              # UTC timezone data link
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
    obs_data =  {'Date(EST)' : [], 'Stage' : []}
    forecast_data = {'Date(EST)' : [], 'Stage' : []}
     
    #---Extract Values to Dictionaries
    value = 'Observed'
    
    for row in data_rows:
        d = row.find_all('td')
        try:
            dtm   = d[0].get_text().split()[0] + '/' + str(year) +' '+ d[0].get_text().split()[1]
            stage = d[1].get_text()
        
            if value == 'Observed':
                obs_data['Date(EST)'].append(dtm) 
                obs_data['Stage'].append(stage)
    
            elif value =='Forecast':
                forecast_data['Date(EST)'].append(dtm) 
                forecast_data['Stage'].append(stage)
    
        except:
            check_value = str(d)
            if 'Forecast  Data ' in check_value:
                value = 'Forecast'
            
    #---Create & Format Dataframes
    df_obs = pd.DataFrame.from_dict(obs_data)
    df_obs['Date(EST)'] = pd.to_datetime(df_obs['Date(EST)'], format='%m/%d/%Y %H:%M')
    df_obs['Stage'] = df_obs['Stage'].astype(str).str[:-2].astype(np.float)    # remove string ft
    df_obs = df_obs.set_index(df_obs['Date(EST)'])
    df_obs = df_obs.iloc[::-1]                                                 #--Reverse rows to get from previous to current date
  
    df_fcst = pd.DataFrame.from_dict(forecast_data)   
    df_fcst['Date(EST)'] = pd.to_datetime(df_fcst['Date(EST)'], format='%m/%d/%Y %H:%M')
    df_fcst['Stage'] = df_fcst['Stage'].astype(str).str[:-2].astype(np.float)
    df_fcst = df_fcst.set_index(df_fcst['Date(EST)'] )
    
#------------------------------------PLOT-------------------------------------#    
    
    
    #--Initialize Plots
    fig, ax = plt.subplots(figsize=(12,6))
    
    #--Plot Observed
    x0 = df_obs['Date(EST)']
    y0 = df_obs['Stage']
    #ax.plot(x0 ,y0, color = 'b')       # Observed

    #--Plot Forecast
    x1 = df_fcst['Date(EST)']
    y1 = df_fcst['Stage']
    #ax.plot(x1 ,y1, color = 'r')       # Observed
    
    ax.plot(x0 ,y0, color = 'b', marker = 'o')       # Add Points
    ax.plot(x1 ,y1, color = 'r', marker = 'o')       # Add Points
    plt.legend(['Observed', 'Forecast'], loc='lower left',scatterpoints = 1)
    plt.title('AHPS Data: {}'.format(gage))
    plt.xlabel('(EST)')
    plt.ylabel('Stage (ft)')
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%b %d %H:%M'))
    plt.gca().xaxis.set_major_locator(HourLocator(np.arange(0, 25, 12)))
    plt.gcf().autofmt_xdate()  
    plt.close()
    
    
#-------------------------------PROCESS OBS DATA------------------------------#        

##--Find out forecast data interval
    if df_fcst.empty == False:
        df_fcst['deltaT'] = df_fcst.index.to_series().diff().dt.seconds.div(60, fill_value=0) # time interval for whole dataset
        dd = int(df_fcst["deltaT"].iloc[-1])   
                                               # value of the time interval (uniform in this data set)
        if dd >= 60:
            dd = int(dd/60)
        else:
            dd = dd
            
        ##--Delete deltaT column
        del df_fcst['deltaT']
        
        ##--Match the interval for observed data with forecast data
        obs_end_date = df_fcst['Date(EST)'].iloc[0] - timedelta(hours = dd)
        obs_end = obs_end_date.strftime(format = '%Y-%m-%d %H:%M:%S')
        
        time1 = df_obs.index[0]
        time2 = obs_end_date
        
        Dtime = time2-time1
        time_comp = Dtime.components
        total_days = (time_comp.days*24 + time_comp.hours)/24
        total_days = math.ceil(total_days)
        
        obs_start_date = obs_end_date - timedelta(total_days) 
        obs_start = obs_start_date.strftime(format = '%Y-%m-%d %H:%M:%S')
        idx2 = pd.date_range(obs_start,obs_end ,freq='{}H'.format(dd))
        df_obs_new = df_obs.reindex(idx2, fill_value = '')
        
        ##-- To remove warning
        del df_obs_new['Date(EST)']
        del df_fcst['Date(EST)']
        
        if df_obs_new['Stage'].iloc[0]=='':
            df_obs_new = df_obs_new[1:]
        
        for i in range (0,len(df_obs_new)):
            if df_obs_new['Stage'].iloc[i] == '':
                df_obs_new['Stage'].iloc[i] = df_obs_new['Stage'].iloc[i-1]
                #df_obs_new['Date(EST)'].iloc[i] = df_obs_new['Date(EST)'].iloc[i-1] + timedelta(hours=dd) 
                
        ##--Append forecast and observation 
        obs_fcst_add = df_obs_new.append(df_fcst)
        obs_fcst_add.index.name = 'Date(EST)'
        #obs_fcst_add['Stage'].plot()
        
    else:
        del df_obs['Date(EST)']
        obs_fcst_add = df_obs
        #obs_fcst_add['Stage'].plot()
        
    return obs_fcst_add       
            