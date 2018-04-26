# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:43:06 2017

@author: selina

"""

import os
import h5py                 #(if h5py is the cause for 'kernel died' pip uninstall h5py from anaconda and then pip install h5py)
#import shutil
import numpy as np
import pandas as pd
from shutil import copyfile
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.offsetbox import AnchoredText
import matplotlib.image as mpimg
import seaborn as sns


os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
from NOAA_data_download import *
from NOAA_data_download_forecast_obs import *

#--Change directory
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')

#--Output file from HEC-RAS to be read in python

#hfile = 'Anacostia_Potomac_version1.p01.hdf'
hfile = 'Anacostia_Potomac_version1.p01.hdf'


#--Channel velocity,flow and water surface elevation

with h5py.File(hfile, 'r') as hf:
    
    elev =     hf['Geometry']['Cross Sections']['Station Elevation Values']
    geom_info= hf['Results']['Unsteady']['Geometry Info']['Cross Section Only']
    node_info= hf['Results']['Unsteady']['Geometry Info']['Node Info']
    
    ch_vel =   hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Cross Sections']['Velocity Channel']
    vel_tot =  hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Cross Sections']['Velocity Total']
    flow1 =    hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Cross Sections']['Flow']
    flow_lat = hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Cross Sections']['Flow Lateral']
    ws_elev =  hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Cross Sections']['Water Surface']
    time =     hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Time']
    dat_tim1 = hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['Time Date Stamp']  
    
    mx_mn_1 =  hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Summary Output']['Cross Sections']['Maximum Channel Velocity']
    mx_mn_2 =  hf['Results']['Unsteady']['Output']['Output Blocks']['DSS Hydrograph Output']['Summary Output']['Cross Sections']['Maximum Channel Velocity'] 
    
    flow2 =    hf['Results']['Unsteady']['Output']['Output Blocks']['DSS Hydrograph Output']['Unsteady Time Series']['Cross Sections']['Flow']
    ws_elev2 = hf['Results']['Unsteady']['Output']['Output Blocks']['DSS Hydrograph Output']['Unsteady Time Series']['Cross Sections']['Water Surface']
    dat_tim2 = hf['Results']['Unsteady']['Output']['Output Blocks']['DSS Hydrograph Output']['Unsteady Time Series']['Time Date Stamp']
    
    dat_tim3 = hf['Results']['Unsteady']['Output']['Output Blocks']['DSS Profile Output']['Unsteady Time Series']['Time Date Stamp']
    DSS_flow = hf['Results']['Unsteady']['Output']['Output Blocks']['DSS Profile Output']['Unsteady Time Series']['Cross Sections']['Flow']
    DSS_ws =   hf['Results']['Unsteady']['Output']['Output Blocks']['DSS Profile Output']['Unsteady Time Series']['Cross Sections']['Water Surface']
    
    geom_info  =  np.array(geom_info)
    node_info  =  np.array(node_info)
                
    ch_vel  =  np.array(ch_vel)
    vel_tot =  np.array(vel_tot)
    flow1   =  np.array(flow1)
    flow_lat =  np.array(flow_lat)
    ws_elev =   np.array(ws_elev)
    time =     np.array(time)
    dat_tim1 = np.array(dat_tim1)
    
    flow2 =    np.array(flow2)
    ws_elev2 =  np.array(ws_elev2)
    dat_tim2 = np.array(dat_tim2)
    
    dat_tim3 =  np.array(dat_tim3)
    DSS_flow  =  np.array(DSS_flow)
    DSS_ws =   np.array(DSS_ws)
    elev  =    np.array(elev)
    
    for index, key in enumerate(geom_info):
        print(key)


#--Convert the required datasets into dataframe
df_ch_vel =  pd.DataFrame.from_dict(ch_vel)
df_DSS_ws =  pd.DataFrame.from_dict(DSS_ws)
df_elev =    pd.DataFrame.from_dict(elev)                                      # cross section station and elevation
df_dat_tim1= pd.DataFrame.from_dict(dat_tim1)
df_geom_info = pd.DataFrame.from_dict(geom_info)
df_ws_elev = pd.DataFrame.from_dict(ws_elev)


#--Format the geometry data for seperating cross section names
df_geom_info = pd.DataFrame.from_dict(geom_info)  
geom_id_list=[]   
for i in range (0,len(df_geom_info)):
    df_geom_info_new = df_geom_info.iloc[i]
    geom_list = list(df_geom_info_new)
    geom_id = str(geom_list).replace('b','').replace('[','').replace(']','').replace('"','"').replace("'","")
    geom_id_list.append(geom_id)
 
   
#--Format dates for plots             
date_time = str(df_dat_tim1).replace('b','').replace("'","").split('\n1', 1)[0].replace('0   ','').split('\n0', 1)[-1].replace("  ","").replace('0\n','').replace('  ','')
date_time_first = datetime.strptime(date_time, "%d%b%Y %H:%M:%S")
intervals=len(df_dat_tim1)
idx = pd.date_range(date_time_first, periods=intervals, freq='H')              # change the freq each time   'H' for hour and 'T' for minutes
idxtest = pd.date_range(date_time_first, periods=intervals, freq='6T')

##--If indexes are not hourly
#idx2 = pd.date_range(idx[0],idx[-1], freq='H')
#idx = idx2

#--Seperate station and elevation data
station=df_elev[0]
elevation=df_elev[1]

#df_elev.to_csv('df_elev.tsv')

#--Loop to get data for each station
df_station=[]
df_station_new=[]
df_each_elev=[]
df_each_station=[]
df_matrix = pd.DataFrame()


#--Add an index to make loop for seperating each station
station_new = station[:]   
last_index = station.index[-1]+1
station_new['{}'.format(last_index)]= 0                                        # 0 added to the end to get all the index

elevation_new=elevation[:]
elevation_new['{}'.format(last_index)]= 0 


###########################################################################
# ??????? 3180 for this cross section only,delete for others# ??????????? #
###########################################################################


#--Save the data for each station
for i in range (len(station_new)):
    if station_new[i]==float(0) or station_new[i]==float(-3180):             
        df_station.append(i)
        df_station_new=pd.DataFrame(df_station)            #list to dataframe
        #df_station_new.iloc[-1]=df_station_new.iloc[-1]-1  #get the end station corrected

        
#--Save stations and elevations for each cross section in csv files
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
j=0
while j<=len(df_station_new)-2:
    df_each_station = pd.DataFrame(station_new[int(df_station_new.iloc[j]):int(df_station_new.iloc[j+1])])
    df_each_elev = pd.DataFrame(elevation_new[int(df_station_new.iloc[j]):int(df_station_new.iloc[j+1])])
    df_each_elev_stat = pd.DataFrame(index=list(range(int(df_station_new.iloc[j]),int(df_station_new.iloc[j+1]))))
    df_each_elev_stat['xs station'] = df_each_station
    df_each_elev_stat['xs elev'] = df_each_elev
    #os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
    #os.chdir('C:\\Users\\admin\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\data')
    df_each_elev_stat.to_csv('cross_section{}.tsv'.format(j),sep='\t',encoding='utf-8',columns=['xs station','xs elev'])
    j=j+1 
         
##########################################################################################################################   
#-------------------------------------------------------------------------------------------------------------------------
##--ADCIRC DATA

url = 'https://raw.githubusercontent.com/MasonFloodHazardsResearchLab/MasonFloodHazardsResearchLab.github.io/master/TabularData/ADCIRC.tsv'
df_adc = pd.read_csv(url,sep="\t")
idx_adc = df_adc['Datetime(UTC)'] 
df_adc.index = pd.to_datetime(idx_adc)
df_adc.index = df_adc.index - timedelta(hours=5)
idx_adc2 = df_adc.index
idx_adc2 = idx_adc2 + timedelta(hours=2)

#df_wav = df_adc['GTND2']
df_wdc = df_adc['WASD2']
df_alx = df_adc['AXTV2']


#--Event names
#if date_time_first.year == 2011:
#    storm = 'Irene'
#elif date_time_first.year == 2003:
#    storm = 'Isabel'    
#elif date_time_first.year == 2012:
#    storm = 'Sandy'  
#else: 
#    storm = 'Random event'

### PLOTS
    
#--Modiy idx to remove past data    
idxx = idx[~(idx <= datetime.now())]
fig_len = 11
fig_wid = 6.5

# plot time interval
plot_interval = 12  

# logo of GMU  
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
logo = mpimg.imread('E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\logo.png')
logo_x = 835
logo_y = 410
## Forecast data
# River XS starts from Anacostia Lower --> Potolmac Upper ---> Potomac Lower 
k = 0
###############################################################################
file_name = 'Little_Falls'
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
#plt.plot(test_data['Stage'])
test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]
#test_data_new = test_data_new
idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)

xs_list = [59]
for j in xs_list: 
    g_id=geom_id_list[j]
    DSS = df_DSS_ws[j] 
                
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    
    DSS1 = df_DSS_ws[j+1]
    DSS2 = df_DSS_ws[j+2]
    DSS4 = df_DSS_ws[j+4]
    DSS6 = df_DSS_ws[j+6]
    DSS7 = df_DSS_ws[j+7]
    DSS8 = df_DSS_ws[j+8]
    DSS10 = df_DSS_ws[j+10]
    DSS12 = df_DSS_ws[j+12]
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()
    
    ax1.plot(idxx, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    
    
#    ax1.plot(idx, DSS1, lw=2,   color='g',label='HECRAS 1 XS D/S')
#    ax1.plot(idx, DSS2, lw=2,   linestyle = '--', color='m',label='HECRAS 2 XS D/S')
#    ax1.plot(idx, DSS4, lw=2,   color='y',label='HECRAS 4 XS D/S')
#    ax1.plot(idx, DSS6, lw=2,   color='c',label='HECRAS 6 XS D/S')
#    ax1.plot(idx, DSS7, lw=3,   linestyle = '--', color='g',label='HECRAS 7 XS D/S')
#    ax1.plot(idx, DSS8, lw=2,   color='k',label='HECRAS 8 XS D/S')
#    ax1.plot(idx, DSS10,lw=2,   color='m',label='HECRAS 10 XS D/S')
#    ax1.plot(idx, DSS12,lw=2,  linestyle = ':', color='k',label='HECRAS 12 XS D/S')
    
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4, color='b',label='AHPS')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    # https://matplotlib.org/examples/color/named_colors.html
    
    
    y1 = 1.524
    y2 = 3.058

    y11 = round(y1/0.3048,1)
    y22 = round(y2/0.3048,1)

    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical
    ax1.axhline(y = y2, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y1, y2, alpha = 0.5, color='yellow') 
    
    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y2, y_max, alpha = 0.5, color='darkorange')
    ax1.annotate('Action: {}m or {}ft'.format(y1,y11), xy = (0,y1), xycoords=("axes fraction","data"))
    #ax1.annotate("Test", xy=(0, 2), xycoords=("axes fraction","data"))
    ax1.annotate('Minor: {}m or {}ft'.format(y2,y22), xy = (0, y2), xycoords=("axes fraction","data"))
    #ax1.grid()  

    ax1.figure.figimage(logo, 835, 410, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE", "OBS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    #legend = ax1.legend(loc='lower right',bbox_to_anchor=(1.12, 0.5), shadow=True, fontsize='x-large')
    #legend.get_frame().set_facecolor('blue')               
    #ax1.text(1, 1, r'Storm: Irene 2011')
    #ax1.legend(['water surface elevation'])
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    #wid = ax1.get_window_extent().width
    #ax1.patch.set_facecolor(bg_color)
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
  
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    #plt.tight_layout(pad=3)
    #ax1.xaxis.labelpad = 5
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name))
    plt.close()

    #DSS.to_csv('cross_section{}.tsv'.format(j),sep='\t',encoding='utf-8',columns=['xs station','xs elev'])
    
###############################################################################
    
file_name = 'Wisconsin_Avenue'
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
#plt.plot(test_data['Stage'])

test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]
idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)

xs_list = [86+k]

for j in xs_list: 
    g_id=geom_id_list[j]  
    #geom_id_list[0]
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    #DSS = DSS + 0.48                  # WL correction 
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()
    
    idxx2 = idxx + timedelta(hours=1)  # time correction
    ax1.plot(idxx2, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4,  color='b',label='AHPS')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    y1 = 1.674
    y2 = 1.8288
    y3 = 2.1336
    
    y11 = round(y1/0.3048,1)
    y22 = round(y2/0.3048,1)
    y33 = round(y3/0.3048,1)
    
    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical
    ax1.axhline(y = y2, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y3, lw = 0.5, color='k', linestyle='-')
    
    ax1.axhspan(y1, y2, alpha = 0.5, color='yellow')
    ax1.axhspan(y2, y3, alpha = 0.5, color='darkorange')
    
    
    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y3, y_max, alpha = 0.5, color='red')
    
    ax1.annotate('Action: {}m or {}ft'.format(y1,y11), xy = (0, y1), xycoords=("axes fraction","data"))
    ax1.annotate('Minor: {}m or {}ft'.format(y2,y22), xy = (0, y2), xycoords=("axes fraction","data"))
    ax1.annotate('Moderate: {}m or {}ft'.format(y3,y33), xy = (0, y3), xycoords=("axes fraction","data"))
    #ax1.grid()  
    
    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE", "OBS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    #ax1.get_legend()
    #ax1.legend(['water surface elevation'])
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    #plt.title('{} ({})'.format(g_id,file_name))
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name))
    plt.close()
    

###############################################################################

file_name = 'Washington_DC'
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
#plt.plot(test_data['Stage'])
test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]
idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)

xs_list = [109+k]

for j in xs_list: 
    g_id=geom_id_list[j]  
    #geom_id_list[0]
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    #DSS = DSS + 0.17
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()
    
    idxx2 = idxx + timedelta(hours=1)
    ax1.plot(idxx2, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4,  color='b',label='AHPS')
    ax1.plot(idx_adc2, df_wdc, lw=2, marker='', markersize = 4,  color='g',label='ADCIRC')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    y1 = 1.128
    y2 = 1.28
    y3 = 1.615
    y4 = 2.134
    
    y11 = round(y1/0.3048,1)
    y22 = round(y2/0.3048,1)
    y33 = round(y3/0.3048,1)
    y44 = round(y4/0.3048,1)
    
    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical
    ax1.axhline(y = y2, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y3, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y4, lw = 0.5, color='k', linestyle='-')
    
    
    ax1.axhspan(y1, y2, alpha = 0.5, color='yellow')
    ax1.axhspan(y2, y3, alpha = 0.5, color='darkorange')
    ax1.axhspan(y3, y4, alpha = 0.5, color='red')
    
    
    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y4, y_max, alpha = 0.5, color='orchid')
    
    ax1.annotate('Action: {}m or {}ft'.format(y1, y11), xy = (0, y1), xycoords=("axes fraction","data"))
    ax1.annotate('Minor: {}m or {}ft'.format(y2, y22), xy = (0, y2), xycoords=("axes fraction","data"))
    ax1.annotate('Moderate: {}m or {}ft'.format(y3, y33), xy = (0, y3), xycoords=("axes fraction","data"))
    ax1.annotate('Major: {}m or {}ft'.format(y4, y44), xy = (0, y4), xycoords=("axes fraction","data"))
    #ax1.grid()  
    
    
    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE", "OBS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    #ax1.legend(['water surface elevation'])
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    #plt.title('{} ({})'.format(g_id,file_name))
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name))
    plt.close()


###############################################################################

file_name = 'Alexandria'
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
#plt.plot(test_data['Stage'])
test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]

idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)
xs_list = [115+k]

for j in xs_list: 
    g_id=geom_id_list[j]  
    #geom_id_list[0]
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    #DSS = DSS - 0.25
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()
    
    idxx2 = idxx + timedelta(hours=1)
    ax1.plot(idxx2, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4, color='b',label='AHPS')
    ax1.plot(idx_adc2, df_alx, lw=2, marker=None, markersize = 4, color='g',label='ADCIRC')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    
    y1 = 0.762
    y2 = 0.945
    y3 = 1.37
    y4 = 2.01
    
    y11 = round(y1/0.3048,1)
    y22 = round(y2/0.3048,1)
    y33 = round(y3/0.3048,1)
    y44 = round(y4/0.3048,1)
    
    
    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical
    ax1.axhline(y = y2, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y3, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y4, lw = 0.5, color='k', linestyle='-')
    
    
    ax1.axhspan(y1, y2, alpha = 0.5, color='yellow')
    ax1.axhspan(y2, y3, alpha = 0.5, color='darkorange')
    ax1.axhspan(y3, y4, alpha = 0.5, color='red')
    
    
    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y4, y_max, alpha = 0.5, color='orchid')
    
    ax1.annotate('Action: {}m or {}ft'.format(y1, y11), xy = (0, y1), xycoords=("axes fraction","data"))
    ax1.annotate('Minor: {}m or {}ft'.format(y2, y22), xy = (0, y2), xycoords=("axes fraction","data"))
    ax1.annotate('Moderate: {}m or {}ft'.format(y3, y33), xy = (0, y3), xycoords=("axes fraction","data"))
    ax1.annotate('Major: {}m or {}ft'.format(y4, y44), xy = (0, y4), xycoords=("axes fraction","data"))
    #ax1.grid() 
    
    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE", "OBS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    #plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name))
    plt.close()

############################################################################### 
  
file_name = 'Dahlgren'
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
#plt.plot(test_data['Stage'])
test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]
idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)
xs_list = [144+k]

for j in xs_list: 
    g_id=geom_id_list[j]  
    #geom_id_list[0]
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()
    
    ax1.plot(idxx, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4,  color='b',label='AHPS')
    #ax1.border_fill_color = "whitesmoke"
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    
    y1 = 0.914
    y2 = 1.067
    y3 = 1.524
    
    y11 = round(y1/0.3048,1)
    y22 = round(y2/0.3048,1)
    y33 = round(y3/0.3048,1)
    
    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical
    ax1.axhline(y = y2, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y3, lw = 0.5, color='k', linestyle='-')
    
    ax1.axhspan(y1, y2, alpha = 0.5, color='yellow')
    ax1.axhspan(y2, y3, alpha = 0.5, color='darkorange')
   
    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y3, y_max, alpha = 0.5, color='red')
    
    ax1.annotate('Action: {}m or {}ft'.format(y1, y11), xy = (0, y1), xycoords=("axes fraction","data"))
    ax1.annotate('Minor: {}m or {}ft'.format(y2, y22), xy = (0, y2), xycoords=("axes fraction","data"))
    ax1.annotate('Moderate: {}m or {}ft'.format(y3, y33), xy = (0, y3), xycoords=("axes fraction","data"))
    #ax1.grid() 
    
    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE", "OBS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name))
    plt.close()
    
###############################################################################
    
file_name = 'Piney_Point'
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]

idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)
xs_list = [150+k]

for j in xs_list: 
    g_id=geom_id_list[j]   ## title only lewisetta 
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    
    DSS5 = df_DSS_ws[j-5]
    DSS10 = df_DSS_ws[j-10]
    DSS15 = df_DSS_ws[j-15]
    DSS25 = df_DSS_ws[j-25]
    DSS30 = df_DSS_ws[j-30]
    DSS35 = df_DSS_ws[j-35]
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()
    
    ax1.plot(idxx, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    
#    ax1.plot(idx, DSS5,  lw=3, linestyle = ':', color='k',label='RAS U/S 5 XS')
#    ax1.plot(idx, DSS10, lw=4, linestyle = '-.', color='g',label='RAS U/S 10 XS')
#    ax1.plot(idx, DSS15, lw=2, linestyle = '--', color='c',label='RAS U/S 15 XS')
#    ax1.plot(idx, DSS25, lw=1, color='g',label='RAS U/S 25 XS')
#    ax1.plot(idx, DSS30, lw=1, color='k',label='RAS U/S 30 XS')
#    ax1.plot(idx, DSS35, lw=2, color='y',label='RAS U/S 35 XS')
    
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4, color='b',label='AHPS')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    
    y1 = 0.762
    y2 = 0.823
    y3 = 1.067
    y4 = 1.524
    
    y11 = round(y1/0.3048,1)
    y22 = round(y2/0.3048,1)
    y33 = round(y3/0.3048,1)
    y44 = round(y4/0.3048,1)
    
    
    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical
    ax1.axhline(y = y2, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y3, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y4, lw = 0.5, color='k', linestyle='-')
    
    
    ax1.axhspan(y1, y2, alpha = 0.5, color='yellow')
    ax1.axhspan(y2, y3, alpha = 0.5, color='darkorange')
    ax1.axhspan(y3, y4, alpha = 0.5, color='red')
    
    
    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y4, y_max, alpha = 0.5, color='orchid')
    
    ax1.annotate('Action: {}m or {}ft'.format(y1, y11), xy = (0, y1), xycoords=("axes fraction","data"))
    ax1.annotate('Minor: {}m or {}ft'.format(y2, y22), xy = (0, y2), xycoords=("axes fraction","data"))
    ax1.annotate('Moderate: {}m or {}ft'.format(y3, y33), xy = (0, y3), xycoords=("axes fraction","data"))
    ax1.annotate('Major: {}m or {}ft'.format(y4, y44), xy = (0, y4), xycoords=("axes fraction","data"))
    #ax1.grid() 
    
    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE", "OBS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    #ax1.legend(['water surface elevation'])
    #ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    #plt.title('{} ({})'.format(g_id,file_name))
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name))
    plt.close()

###############################################################################
   
file_name = 'Lewisetta'
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
#plt.plot(test_data['8635750'])
test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]

idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)
xs_list = [154+k]

for j in xs_list: 
    g_id=geom_id_list[j]   ## title only lewisetta 
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    
    DSS5 = df_DSS_ws[j-5]
    DSS10 = df_DSS_ws[j-10]
    DSS15 = df_DSS_ws[j-15]
    DSS25 = df_DSS_ws[j-25]
    DSS30 = df_DSS_ws[j-30]
    DSS35 = df_DSS_ws[j-35]
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()
    
    ax1.plot(idxx, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    
#    ax1.plot(idx, DSS5,  lw=3, linestyle = ':', color='k',label='RAS U/S 5 XS')
#    ax1.plot(idx, DSS10, lw=4, linestyle = '-.', color='g',label='RAS U/S 10 XS')
#    ax1.plot(idx, DSS15, lw=2, linestyle = '--', color='c',label='RAS U/S 15 XS')
#    ax1.plot(idx, DSS25, lw=1, color='g',label='RAS U/S 25 XS')
#    ax1.plot(idx, DSS30, lw=1, color='k',label='RAS U/S 30 XS')
#    ax1.plot(idx, DSS35, lw=2, color='y',label='RAS U/S 35 XS')
    
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4, color='b',label='AHPS')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    
    y1 = 0.762
    y2 = 0.914
    y3 = 1.067
    y4 = 1.22
    
    y11 = round(y1/0.3048,1)
    y22 = round(y2/0.3048,1)
    y33 = round(y3/0.3048,1)
    y44 = round(y4/0.3048,1)
    
    
    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical
    ax1.axhline(y = y2, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y3, lw = 0.5, color='k', linestyle='-')
    ax1.axhline(y = y4, lw = 0.5, color='k', linestyle='-')
    
    
    ax1.axhspan(y1, y2, alpha = 0.5, color='yellow')
    ax1.axhspan(y2, y3, alpha = 0.5, color='darkorange')
    ax1.axhspan(y3, y4, alpha = 0.5, color='red')
    
    
    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y4, y_max, alpha = 0.5, color='orchid')
    
    ax1.annotate('Action: {}m or {}ft'.format(y1, y11), xy = (0, y1), xycoords=("axes fraction","data"))
    ax1.annotate('Minor: {}m or {}ft'.format(y2, y22), xy = (0, y2), xycoords=("axes fraction","data"))
    ax1.annotate('Moderate: {}m or {}ft'.format(y3, y33), xy = (0, y3), xycoords=("axes fraction","data"))
    ax1.annotate('Major: {}m or {}ft'.format(y4, y44), xy = (0, y4), xycoords=("axes fraction","data"))
    #ax1.grid() 
    
    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE", "OBS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    #ax1.legend(fancybox=True, framealpha=3, shadow=True, borderpad=1)
    #ax1.legend(['water surface elevation'])
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    #plt.title('{} ({})'.format(g_id,file_name))
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name))
    plt.close()   

###############################################################################

file_name = 'Bladensburg' # Observed WSE
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
##plt.plot(test_data['8635750'])
test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]

idx_new = test_data['Date(EST)']
idx2 = pd.DatetimeIndex(idx_new)
file_name2 = 'Bladensburg' # HECRAS WSE

xs_list = [3]  # no change in aquatic garden xs number

for j in xs_list: 
    g_id=geom_id_list[j]  
    #geom_id_list[0]
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    DSS = DSS - 0.43  ##testing with the subtraction of a constant value
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()

    ax1.plot(idxx, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    ax1.plot(idx2, test_data_new, lw=1, marker='o', markersize = 4, color='b',label='AHPS')
    #ax1.plot(idx, test_data_new, lw=2, marker='*', color='b')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines----------------------------#

    #----------------NO data available for flood stage------------------------#

    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    #ax1.text(0.1,0.1,'AHPS Forecast Data Missing', style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    #ax1.legend(fancybox=True, framealpha=3, shadow=True, borderpad=1)
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    #plt.title('{} ({})'.format(g_id,file_name))
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour = range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name2))
    plt.close()

###############################################################################

file_name = 'Aquatic_Garden' # Observed WSE
file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}.tsv'.format(file_name)
#test_data = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
##plt.plot(test_data['8635750'])
#test_data_new = test_data['Stage']
#test_data_new = test_data_new[:-1]

#idx_new = test_data['Date(EST)']
#idx2 = pd.DatetimeIndex(idx_new)
file_name2 = 'Aquatic_Garden' # HECRAS WSE

xs_list = [21]  # no change in aquatic garden xs number

for j in xs_list: 
    g_id=geom_id_list[j]  
    #geom_id_list[0]
    DSS = df_DSS_ws[j]
    nval = len(idx)-len(idxx)
    DSS = DSS[nval:]
    
    plt.style.use('seaborn-darkgrid')
    fig,ax1 = plt.subplots(1, 1, figsize=(fig_len, fig_wid), dpi=100)
    ax1.grid()

    ax1.plot(idxx, DSS, lw=1, marker='o', markersize = 4, color='r',label='Mason')
    #ax1.plot(idx2, test_data_new, lw=2, marker='o', markersize = 4, color='b',label='AHPS')
    #ax1.plot(idx, test_data_new, lw=2, marker='*', color='b')
    ax1.axvline(pd.to_datetime(datetime.now()), color='k', linestyle='--', lw = 0.8)
    
    #---------------------- Plot flood stage lines-----------------------------
    
    # https://matplotlib.org/users/recipes.html
    
    y1 = 1.067
    y11 = round(y1/0.3048,1)
    
    ax1.axhline(y = y1, lw = 0.5, color='k', linestyle='-')  # plot horizontal line--'axvline' for vertical

    y_max = ax1.get_ylim()[1]
    plt.gca().set_ylim(top=y_max)  
    ax1.axhline(y = y_max, lw = 0.5, color='k', linestyle='-')
    ax1.axhspan(y1, y_max, alpha = 0.5, color='yellow')
    ax1.annotate('Action: {}m or {}ft'.format(y1, y11), xy = (0, y1), xycoords=("axes fraction","data"))
    
    ax1.figure.figimage(logo, logo_x, logo_y, alpha=0.4, zorder=1)
    plt.xticks(rotation=0)
    #plt.legend(["HECRAS WSE"],title='Storm : {} {}'.format(storm,date_time_first.year))
    #ax1.text(0.1,0.1,'AHPS Forecast Data Missing', style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(1.12, 0.5),fancybox=True, shadow=True, ncol=1,fontsize=10)
    #ax1.legend(['water surface elevation'])
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (meter)')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    #plt.title('{} ({})'.format(g_id,file_name))
    plt.text(datetime.now() + timedelta(hours=12),1,'NO AHPS DATA AVAILABLE', color='magenta', fontsize=16,fontweight='bold')
    plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=16, fontweight='bold')
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval = plot_interval))
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(file_name2))
    plt.close()
    
###############################################################################
#     ENSEMBLE: https://www.weather.gov/erh/mmefs_marfc?id=HNKM2&model=SREF   
#     Interactive map: https://plot.ly/javascript/time-series/
#     https://plot.ly/javascript/          
#     https://codepen.io/plotly/pen/NvazKR 
#     kml attributes:   https://stackoverflow.com/questions/42516114/geoxml3-accessing-kml-attribute-datas
#     https://developers.google.com/kml/documentation/extendeddata#entity-replacement-for-extended-data-elements                                
###############################################################################

## Selected cross section velocity and water level table
#WSE_alldata = pd.DataFrame()
#VEL_alldata = pd.DataFrame()
#
#WSE_alldata['LF'] = df_DSS_ws[59] 
#VEL_alldata['LF'] = df_ch_vel[59]  
#
#WSE_alldata['WAV'] = df_DSS_ws[86] 
#VEL_alldata['WAV'] = df_ch_vel[86]
#
#WSE_alldata['WDC'] = df_DSS_ws[109] 
#VEL_alldata['WDC'] = df_ch_vel[109]
#
#WSE_alldata['ALEX'] = df_DSS_ws[115] 
#VEL_alldata['ALEX'] = df_ch_vel[115]
#
#WSE_alldata['DAHL'] = df_DSS_ws[144] 
#VEL_alldata['DAHL'] = df_ch_vel[144]
#
#WSE_alldata['PINY'] = df_DSS_ws[150] 
#VEL_alldata['PINY'] = df_ch_vel[150]
#
#WSE_alldata['LWT'] = df_DSS_ws[154] 
#VEL_alldata['LWT'] = df_ch_vel[154]
#
#WSE_alldata['BLD'] = df_DSS_ws[3] 
#VEL_alldata['BLD'] = df_ch_vel[3]
#
#WSE_alldata['AQUA'] = df_DSS_ws[21] 
#VEL_alldata['AQUA'] = df_ch_vel[21]

###############################################################################

##--Plot the cross sections with water level (shaded area)
##--Loop for selected cross sections 
col=len(df_DSS_ws.columns)
row=len(df_DSS_ws.index)
wse=[]
wse_col_row=[]

g_id2=list()       
wse_list=[115+k] # need to fix the loop for multiple cross sections [0,68,136,171,214,238]     # indexes of the required cross sections for water level
                                                                                   
for j in wse_list:
    #--Read the csv files saved earlier
    file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\cross_section{}.tsv'.format(j)      
    df_read_csv = pd.read_csv(file_path,sep='\t',index_col=None)
    wse_col = df_DSS_ws[j]
    g_id=geom_id_list[j]
    g_id2.append(g_id)
 
    for k in range (0,row):
        a = np.zeros(shape=(row,len(df_read_csv)))
        wse_col_row = wse_col[k]
        wse = [wse_col_row]*len(df_read_csv)
        df_matrix=pd.DataFrame()
        df_matrix['water_level'] = wse            
        df_matrix['stat_elev'] = df_read_csv['xs elev'].tolist()                           # convert series type to list
        #df_matrix.index = df_read_csv['xs station'].index.tolist()
        df_matrix.index = df_read_csv['xs station']
        x = np.array(df_matrix.index) #Convert index (pandas datatype) to numpy array, for ease of plotting 
        y1 = df_matrix['stat_elev']   #Convert dataframe object to numpy array, for ease of plotting
        y2 = df_matrix['water_level'] #Convert dataframe object to numpy array, for ease of plotting

        #--Change directory to the repos to upload
        os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate\\plots_for_video')
        
        plt.style.use('seaborn-darkgrid')
        fig,ax2 = plt.subplots(1, 1,figsize=(9.5, 6.5), dpi=100)                          # initialize plot, figure
        #ax2.grid()
        #ax2.grid(False)
        #plt.axis('off')
        ax2.figure.figimage(logo, 705, 410, alpha=0.3, zorder=1)
        ax2.plot(x, y1,  color='black')                                                   # plot 
        ax2.fill_between(x, y1, y2 = wse_col[0], where=y2>y1, interpolate=True)           # fill up the water
        #ax2.legend(['Water surface elevation in the cross section'])
        ax2.set_xlabel('Cross Section Station (meter)')
        ax2.set_ylabel('Water Surface Elevation (meter)')
        #for i in range (0,len(wse_col)):
        plt.title('{}'.format(g_id) + '\n' + 'Date:{}'.format(idx[k]), backgroundcolor = 'navy', color='white', fontsize=14, fontweight='bold')
        #ax2.grid()
        #plt.title('Forecast at {} ({})'.format(g_id,file_name), backgroundcolor = 'navy', color='white', fontsize=14, fontweight='bold')
        fig.savefig('figure_{}_{}.JPEG'.format(j,k)) 
        #????? JPEG or png ?????? as needed
        plt.close()
        
##--Save the required csv files for water level video to github folder
#place = [59,86,109,115,144,150,154,3,21]
#for k in xslist:
#    for m in place:
#        src = 'E:/Selina/REALTIME_UPDATED_AND_OLD_FILES_HERE/REALTIME_RAS/Seth_Potomac_Anacostia/VERSION0_MODEL_DEC2017_automate/cross_section{}.tsv'.format(k)
#        dst = 'C:/Users/admin/MasonFloodHazardsResearchLab.github.io/potomac_total_water/images/{}.tsv'.format(m)
#        copyfile(src,dst)

#--Delete all csv files from folder
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
#os.chdir('C:\\Users\\admin\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\data')

j=0
while j<=len(df_station_new)-2:
    os.remove('cross_section{}.tsv'.format(j))
    j=j+1