# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:43:06 2017

@author: selina
"""

import os
import h5py                 #(if h5py is the cause for 'kernel died' pip uninstall h5py from anaconda and then pip install h5py)
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.image as mpimg
import seaborn as sns

os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
from NOAA_data_download import *

#--Change directory

os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')

#--Output file from HEC-RAS to be read in python

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
    flow_lat=  np.array(flow_lat)
    ws_elev=   np.array(ws_elev)
    time =     np.array(time)
    dat_tim1 = np.array(dat_tim1)
    
    flow2 =    np.array(flow2)
    ws_elev2=  np.array(ws_elev2)
    dat_tim2 = np.array(dat_tim2)
    
    
    dat_tim3=  np.array(dat_tim3)
    DSS_flow=  np.array(DSS_flow)
    DSS_ws =   np.array(DSS_ws)
    elev  =    np.array(elev)
    
    for index, key in enumerate(geom_info):
        print(key)

#--Convert the required datasets into dataframe
df_DSS_ws =  pd.DataFrame.from_dict(DSS_ws)
df_elev =    pd.DataFrame.from_dict(elev)           # cross section station and elevation
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
date_time = str(df_dat_tim1).replace('b','').replace("'","").split('\n1', 1)[0].replace('0   ','').split('\n0', 1)[-1].replace("  ","").replace('0\n','')
date_time_first = datetime.strptime(date_time, "%d%b%Y %H:%M:%S")
intervals=len(df_dat_tim1)
idx = pd.date_range(date_time_first, periods=intervals, freq='H')  #???? change the freq each time 


#--Seperate station and elevation data
station=df_elev[0]
elevation=df_elev[1]

#df_elev.to_csv('df_elev.csv')

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
    #os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\version1_to_upload')
    df_each_elev_stat.to_csv('cross_section{}.csv'.format(j),sep='\t',encoding='utf-8',columns=['xs station','xs elev'])
    j=j+1 
    
    
 
#######################################################################################################################################################    
#--Read the csv files for required cross section 
#--Loop for all cross sections
#    
#j=0
#while j<=len(df_station_new)-2:
#    file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\version1_to_upload\cross_section{}.csv'.format(j)      
#    df_read_csv = 'dff{}'.format(j)
#    df_read_csv = pd.read_csv(file_path,sep='\t',index_col=None)
#    j=j+1
#    
#--Loop for some cross sections
#file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\version1_to_upload\cross_section{}.csv'.format(1)      
#df_read_csv = pd.read_csv(file_path,sep='\t',index_col=None)
#
#             
#--Water level data format for each cross section stations
#--Loop for all the cross sections       
#DSS = df_DSS_ws [-1]        
#for j in range (0,col):
#    wse_col = df_DSS_ws[j]
#    for k in range (0,row):
#        wse_col_row = wse_col[k]
#        wse = [wse_col_row]*length_elev
#        
######################################################################################################################################################


###############################All figures should be of same size,otherwise video makes problem ######################################################

#--NOAA gage names (see in NOAA data download) 
lwt='LWTV2'                                             # Potomac Lewisetta
alex = 'AXTV2'                                          # Potomac Alexandria   
gtwn ='GTND2'                                           # potomac Wisconsin Ave, Georgetown
l_falls = 'BRKM2'                                       # Potomac Little Falls
hyat='ACOM2'                                            # Anacostia hyattsville, MD                     (NW)
bren='BNTM2'                                            # Anacostia North Brentwood, MD                 (NW)                                   
bladen='BLDM2'                                          # Anacostia Bladenburg, MD                     (Lower)
aqua='ANAD2'                                            # Anacostia Aquatic garden, DC                 (Lower)
rvrdal='RVDM2'                                          # Anacostia Riverdale, MD                    (Northeast)

chvr='CHVM2'
mach_ck = 'NCDV2'
anapolis = 'APAM2'
cbbt = 'CBBV2'
wadc ='WASD2'
ncd='NCDV2'

#gage = [alex,hyat] # selected gage
gage=alex

#for jj in gage:
df = NOAA(gage)
#df = NOAA(jj)
#df[i] = df1
#df['deltaT'] = df.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
#dd4=int(df["deltaT"].iloc[-1])              # indexing the time for date interval
df = df.reindex(idx, fill_value='')
gage214_data = list(df['Stage'])
#gage214_data=[round(float(i), 3) for i in gage214_data]
#print(df.iloc[-1])
#fig,ax1 = plt.subplots(1, 1, figsize=(10, 5.5), dpi=100)
#ax1.plot(idx, gage214_data, lw=2, marker='o', color='r')


##test for comparison on graph (near alex 104)
gage_test = lwt
dff = NOAA(gage_test)
dff = dff.reindex(idx, fill_value='0')
alex_df = dff['Stage']
gage142_data = list(dff['Stage'])

#DSS_alex = df_DSS_ws[104]
#fig,ax1 = plt.subplots(1, 1, figsize=(10, 5.6), dpi=100)
#ax1.plot(idx, DSS_alex, lw=2, marker='o', color='r')
#ax1.plot(idx, alex_df, lw=2, marker='o', color='r')


#--Plot of water level with dates
#--Change directory to the repos to upload
#os.chdir('C:\\Users\\admin\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
xs_list=[0,68,136,104,140,141,142]    # selected cross section index
xs_list=[104] 
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
logo=mpimg.imread('logo.png')

# 0---NW ANA 1.75
# 68--NE ANA 1.99
# 136--LOWER ANA 5.94 (Aquatic)
# 171--UPPER POTO 235353.0 
# 214--LOWER POTO 176580.9 (Alex)
# 238--LOWER POTO 8182.078
df_date_wse = pd.DataFrame()

ii=1
for j in xs_list: 
    g_id=geom_id_list[j]  
    #geom_id_list[0]
    DSS = df_DSS_ws[j]
    fig,ax1 = plt.subplots(1, 1, figsize=(10, 5.6), dpi=100)
    ax1.plot(idx, DSS, lw=2, marker='o', color='r')
    #if j == 104 and gage==alex:
    #ax1.plot(idx, gage214_data, lw=2, marker='o', color='r') 
    #if j==136 and gage==hyat:
        #ax1.plot(idx, gage214_data, lw=2, marker='*', color='b') 
    plt.xticks(rotation=0)
    #ax1.legend(['water surface elevation'])
    ax1.grid()
    ax1.set_xlabel('EST time')
    ax1.set_ylabel('Water surface elevation (ft)')
    ax1.figure.figimage(logo, 2, 2, alpha=0.15, zorder=1)
    #current_palette = sns.color_palette("Paired")
    #sns.set_palette(current_palette)
    ax1.style.use('fivethirtyeight')
    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
    ax1.xaxis.set_major_formatter(xfmt)
    plt.title('{}'.format(g_id))
    #fig.savefig('wse_{}.png'.format(g_id))
    #plt.grid(True)
    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(10)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%I%p\n%a\n%b%d'))
    plt.gca().xaxis.set_major_locator(HourLocator(byhour=range(24), interval=4))
    os.chdir('C:\\Users\\admin\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')
    fig.savefig('figure_{}.png'.format(ii))
    ii=ii+1 
   # plt.close()
    ##----upload time series data in tsv format
    df_date_wse['date'] = idx
    df_date_wse['wse'] = [round(float(i), 2) for i in DSS]
    os.chdir('C:\\Users\\admin\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water')
    df_date_wse.to_csv('cross_section{}.csv'.format(j),sep='\t',encoding='utf-8',columns=['date','wse'])
 # col_names or columns ????  check
    fig('seaborn')
#######################################################################
   
#    g_id11=geom_id_list[104]  
#    DSS11 = df_DSS_ws[104]
#    fig,ax11 = plt.subplots(1, 1, figsize=(10, 5.6), dpi=100)
#    ax11.plot(idx, DSS11, lw=2, marker='o', color='r')
#    #if j == 104 and gage==alex:
#    #ax1.plot(idx, gage214_data, lw=2, marker='o', color='r') 
#    #if j==136 and gage==hyat:
#        #ax1.plot(idx, gage214_data, lw=2, marker='*', color='b') 
#    plt.xticks(rotation=0)
#    #ax1.legend(['water surface elevation'])
#    ax1.grid()
#    ax1.set_xlabel('EST time')
#    ax1.set_ylabel('Water surface elevation (ft)')
#    xfmt = mdates.DateFormatter('%b%d %I:%m%p')
#    ax1.xaxis.set_major_formatter(xfmt)
#    plt.title('{}'.format(g_id))

######################################################################



#--Plot the cross sections with water level
#--Loop for selected cross sections 
col=len(df_DSS_ws.columns)
row=len(df_DSS_ws.index)
wse=[]
wse_col_row=[]

g_id2=list()       
wse_list=[104] # need to fix the loop for multiple cross sections [0,68,136,171,214,238]     # indexes of the required cross sections for water level
                                                                                   
for j in wse_list:
    #--Read the csv files saved earlier
    file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\cross_section{}.csv'.format(j)      
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
        df_matrix['stat_elev'] = df_read_csv['xs elev'].tolist()                     # convert series type to list
        df_matrix.index = df_read_csv['xs station'].index.tolist()
        x = np.array(df_matrix.index) #Convert index (pandas datatype) to numpy array, for ease of plotting 
        y1 = df_matrix['stat_elev']   #Convert dataframe object to numpy array, for ease of plotting
        y2 = df_matrix['water_level'] #Convert dataframe object to numpy array, for ease of plotting

        #--Change directory to the repos to upload
        os.chdir('C:\\Users\\admin\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\videos\\plots_for_video')
        fig,ax2 = plt.subplots(1, 1,figsize=(10, 5.6), dpi=100)                          # initialize plot, figure
        ax2.plot(x, y1,  color='black')                                                # plot 
        ax2.fill_between(x, y1, y2=wse_col[0], where=y2>y1, interpolate=True)          # fill up the water
        ax2.legend(['Water surface elevation in the cross section'])
        ax2.grid()
        ax2.set_xlabel('Station')
        ax2.set_ylabel('Elevation(ft)')
        #for i in range (0,len(wse_col)):
        plt.title('{}'.format(g_id) + '\n' + 'Date:{}'.format(idx[k]))
        fig.savefig('figure_{}_{}.JPEG'.format(j,k)) 
        #????? JPEG or png ?????? as needed
        plt.close()
        
#--Delete all csv files from folder
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
j=0
while j<=len(df_station_new)-2: 
    os.remove('cross_section{}.csv'.format(j))
    j=j+1