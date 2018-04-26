# -*- coding: utf-8 -*-

"""
Created on Thu Apr 27 16:49:35 2017

@author: Selina

"""

import os
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')


import math
import pandas as pd
import numpy as np
from USGS_Data_Grabber import *
from USGS_Data_Grabber_test import *
from NOAA_data_download_forecast import *
from NOAA_data_download_forecast_obs import *
from NOAA_data_download_no_flow import *
from TIDES_CURRENTS_NOAA import*
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


##--------Check working directory and change the directory as required----------------##
#os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\version1_to_upload\\version1_test2')
#---Set paths, filenames
wk_dir = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate'
in_file = os.path.join(wk_dir, r'plan_template_anacostia_potomac.txt')
out_file = os.path.join(wk_dir, r'Anacostia_Potomac_version1.p01')
f = 'Anacostia_Potomac_version1.u01'                                                            # Ouput Unsteady Flow FIle
proj = 'Anacostia_Potomac_version1.prj'


#--NOAA Tide and Currents Station ID    
tide_gage = '8635750' # Lewisetta

#--NOAA gage names (see in NOAA data download) 
bld = 'BLDM2'
lwt = 'LWTV2'
ncd = 'NCDV2'
alex = 'AXTV2'    
cbbt = 'CBBV2'
wadc ='WASD2'
gtwn ='GTND2'
l_falls = 'BRKM2'
mach_ck = 'NCDV2'
anapolis = 'APAM2'                                                                                          
aqua='ANAD2'

#--Select gages from NOAA and USGS
gage_1 = "01651000"    # NW Anacostia      (flow-USGS)
gage_2 = "01649500"    # NE Anacostia      (flow-USGS)                                                                                                                            
###----gage_1 flow + gage_2 flow = Anacostia Lower flow----###

#---Select USGS parameter 
flow  = "00060"
stage = "00065"
elev = "62620"


## STORM DURATION:

df3 = NOAA_forecast(l_falls) 
df4 = NOAA_forecast(lwt)

common_start = max(df3['Date(EST)'].iloc[0],df4['Date(EST)'].iloc[0])
t_y0 = common_start.year
t_m0 = common_start.month
t_d0 = common_start.day
t_hr0 = common_start.hour

common_end = min(df3['Date(EST)'].iloc[-1],df4['Date(EST)'].iloc[-1])
t_y1 = common_end.year
t_m1 = common_end.month
t_d1 = common_end.day
t_hr1 = common_end.hour


#--Datetime for data download
storm_start_date = datetime(t_y0,t_m0,t_d0,t_hr0,0,0)    ## Time Zone: EST 
storm_end_date = datetime(t_y1,t_m1,t_d1,t_hr1,0,0)      ## Time Zone: EST 


#--Datetime for USGS data download (EST)
y0, m0 ,d0 = storm_start_date.year, storm_start_date.month, storm_start_date.day    # Start date (year, month, day)
y1, m1 ,d1 = storm_end_date.year, storm_end_date.month, storm_end_date.day          # End date


#--Format datetime objects, create input line (insert_line)
ras_start = storm_start_date.strftime(format = '%d%b%Y')
ras_end = storm_end_date.strftime(format = '%d%b%Y')


# Fix the gage data start time and end time 
start_index = storm_start_date.strftime(format = '%Y-%m-%d %H:%M:%S')
end_index = storm_end_date.strftime(format = '%Y-%m-%d %H:%M:%S')                   # end date for the index with hr,min and sec


#--Fix the simulation time window
sim_start_hr = '%02d' % storm_start_date.hour
sim_start_min = '%02d' % storm_start_date.minute


sim_end_hr =  '%02d' % storm_end_date.hour                   # simulation hour in 00:00 format
sim_end_min = '%02d' % storm_end_date.minute                                        # simulation minute in 00:00 format
                   
                   
# Simulation date, hour, minute
insert_line = 'Simulation Date=' + str(ras_start) +',{}:00,'.format(sim_start_hr) + str(ras_end) + ',{}:00\n'.format(sim_end_hr)


###############################################################################
#                                                                             #
#                              GAGE-1                                         #
#                                                                             #
###############################################################################



### TRY1 With USGS combined flow
## Gage 1
f1 = datetime.now()- timedelta(hours=2)
f0 = f1-timedelta(days = 2.5)

f11 = f1.strftime(format = '%Y-%m-%d %H:%M:%S')   # EST
f00 = f0.strftime(format = '%Y-%m-%d %H:%M:%S')   # EST

#--Datetime for USGS data download (EST)
y_f0, m_f0, d_f0 = f0.year, f0.month, f0.day    # Start date (year, month, day)
y_f1, m_f1, d_f1 = f1.year, f1.month, storm_end_date.day          # End date

#---Get Gage 1 Data (df1 for flow) [cfs]
df1 = GrabData(gage_1, y_f0, m_f0, d_f0, y_f1, m_f1, d_f1, flow)
df1 = df1*0.0283  # convert cfs to cms (0.0283)                                                                                    
df1_last = df1['StreamFlow'].iloc[-1]
df1_last = round(float(df1_last),3)


#---Get the time interval of data
df1['deltaT'] = df1.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd1=int(df1["deltaT"].iloc[-1])  


## Gage 2
#---Get Gage 2 Data (df2 for Stage)[cfs]
df2 = GrabData(gage_2, y_f0, m_f0, d_f0, y_f1, m_f1, d_f1,flow)
df2 = df2*0.0283
df2_last = df2['StreamFlow'].iloc[-1].round(3)


#---Get the time interval of data
df2['deltaT'] = df2.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd2 = int(df2["deltaT"].iloc[-1])                                                     # value of the time interval (uniform in this data set)
#--Handling the missing values in usgs gage data
#idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd2))              # indexing the time for date interval
df2 = df2.reindex(df1.index, fill_value = '')
for i in range (0,len(df2)):
    if df2['StreamFlow'].iloc[i] == '':
        df2['StreamFlow'].iloc[i] = df2['StreamFlow'].iloc[i-1]

gage1_2_data_test =  list(df1['StreamFlow'] + df2['StreamFlow'])               # converted df1 and df2 from cfs to cms (0.0283)
idx_15T = pd.date_range(start_index, end_index, freq='15T')
length_df1 = len(gage1_2_data_test)-len(idx_15T)
#gage1_2_data_test.dropna()

dd1 = 15
gage1_2_data_test = df1_last + df2_last
gage1_2_data_test = [gage1_2_data_test]*len(idx_15T)
gage1_2_data_test = [round(float(i),3) for i in gage1_2_data_test]
#gage1_2_data_test = gage1_2_data_test[length_df1:]
gage_1_data = gage1_2_data_test # gage_1_data name not changed as the combined flow is assumed in gage_1

     
#---------------------------------------------------------------------------------
#### TRY2 WITH NOAA data
#gage = bld
#
##---Get Gage 1 Data (df1 for flow) [cfs]
#df1 = NOAA_forecast_obs(gage)
#df1.index = df1['Date(EST)']  
#                                                    
##---Get the time interval of data
##df1['deltaT'] = df1.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
##dd1 = int(df1["deltaT"].iloc[-1])                                                   # value of the time interval (uniform in this data set)
##--Handling the missing values in usgs gage  data
##start_index = start_date.strftime(format = '%Y-%m-%d 00:00:00')                     # start date for the corrected time index including missing data date
#df1_new = pd.DataFrame()
#df1_new['Stage'] = df1['Stage']*0.3048 
#df1_new.index = df1['Date(EST)'] 
##df1_new.index = df1_new.index + timedelta(2) + timedelta(hours=15) + timedelta(minutes=5)
#idx_hr = pd.date_range(start_index, end_index, freq='15T')                           # indexing the time for date interval
#length_df1 = len(df1)-len(idx_hr)
#df1_new = df1_new.iloc[length_df1:]
#df1_new.index = idx_hr
#
#dd1= df1_new.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
#dd1 = int(dd1.iloc[-1])  
#
### HOUR or MIN in unsteady flow file
#if dd1>=60:
#    dd1 = int(dd1/60)
#else:
#    dd1 = dd1
#
##---Get the streamflow data from whole data frame                                                                                                                                    # Plot gage data
#gage_1_data = list(df1_new['Stage']) 
#gage_1_data = [round(float(i), 3) for i in gage_1_data]
#


## BLADENSBURG
#del df1_new['deltaT']
gage = bld
df1_BLD = NOAA_forecast_obs(gage) # ?????????
df1_BLD.index = df1_BLD['Date(EST)']
df1_BLD.index.name = 'Date(EST)' 
df1_BLD2 = df1_BLD.round(3)
#df1_BLD2.index = df1_BLD2.index + timedelta(3)-timedelta(hours=9)
#del df1_BLD2['Date(EST)']
df1_BLD2['Stage'] = df1_BLD2['Stage']*0.3048
df1_BLD2.to_csv('Bladensburg.csv', sep='\t',encoding='utf-8')

idx_hr = pd.date_range(start_index, end_index, freq='H')

 
###############################################################################
#                                                                             #
#                                 GAGE-3                                      #
#                                                                             #
###############################################################################
gage = l_falls 
#---Get Gage 3 Data (df3 for Stage) [ft]
df3 = NOAA_forecast(gage) 
df3['Flow'] = df3['Flow'].map(lambda x: x.lstrip('+-').rstrip('kcfs'))
df3['Flow'] = df3['Flow'].astype(float)*1000 # convert kcfs to cfs
#--Delete flow column
del df3['Stage'] 
df3_new = pd.DataFrame()
df3.index = df3['Date(EST)']  
idx_hr = pd.date_range(start_index, end_index, freq='H') 
#df3 = df3.reindex(idx_hr, fill_value = '')
                                                          
#---Get the time interval of data
df3['deltaT'] = df3.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd3 = int(df3["deltaT"].iloc[-1])                                                   # value of the time interval (uniform in this data set)
dd3 = df3.index.to_series().diff().dt.seconds.div(60, fill_value=0) 
dd3 = int(dd3.iloc[-1])  

if dd3 >= 60:
    dd3 = int(dd3/60)
else:
    dd3 = dd3

#---Get the Stage data from whole data frame 
##Assuming that 60% water is flowing downstream and 40% going to aqueduct                                                                       
#-----------------------------------------------------------------------------
gage_3_data = list(df3['Flow']*0.0283)  # convert cfs to cms (0.0283)
#-----------------------------------------------------------------------------      
gage_3_data = [round(float(i), 1) for i in gage_3_data]
                                                                      

## LITTLE FALLS
df3_LF = pd.DataFrame()
gage = l_falls
df3 = NOAA_forecast(gage)
df3_LF['Stage'] = df3['Stage']*0.3048 #meter
idx = df3['Date(EST)']
df3_LF.index = idx
df3_litfals = df3_LF.round(3)
df3_litfals.to_csv('Little_Falls.csv', sep='\t',encoding='utf-8' )

## WISCONSIN AVENUE 
gage = gtwn
df3_WA2 = pd.DataFrame()
df3_WA =  NOAA_forecast(gage) #stage in ft
df3_WA2['Stage'] = df3_WA['Stage']*0.3048 #meter
idx = df3_WA['Date(EST)']
df3_WA2.index = idx
df_Wis_Ave = df3_WA2.round(3)
df_Wis_Ave.to_csv('Wisconsin_Avenue.csv',sep='\t',encoding='utf-8')


## ALEXANDRIA
gage = alex
df3_alex2 = pd.DataFrame()
df3_alex = NOAA_forecast(gage)  #stage in ft time EDT
df3_alex2['Stage'] = df3_alex['Stage']*0.3048
idx = df3_alex['Date(EST)']  
df3_alex2.index = idx
df_alexandria = df3_alex2.round(3)
df_alexandria.to_csv('Alexandria.csv',sep='\t',encoding='utf-8')


###############################################################################
#                                                                             #
#               GAGE-4  (USGS or NOAA data for downstream boundary)           #
#                                                                             #
###############################################################################

gage_4 = lwt
## UTC time for NOAA tides and currents
df4 = NOAA_forecast(gage_4)
del df4['Flow']
df4.index = df4['Date(EST)'] 
#---Get the time interval of data [ft]
df4['deltaT'] = df4.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd4 = int(df4["deltaT"].iloc[-1])                                                   # value of the time interval (uniform in this data set)

if dd4 >= 60:
    dd4 = int(dd4/60)
else:
    dd4 = dd4
    
idx_hr = pd.date_range(start_index, end_index, freq='H')     
df4 = df4.reindex(idx_hr, fill_value="")

#---Get the flow data from whole data frame 
#------------------------------------------------------------------------------
gage_4_data = list(df4['Stage']*0.3048)  # in meter / no need to convert ft to meter (0.3048)
#------------------------------------------------------------------------------
#if gage_4_data[0]=='':
#    gage_4_data[0]= gage_4_data[1]
#for i in range(0,len(gage_4_data)):
#    if gage_4_data[i]=='': 
#        gage_4_data[i]= gage_4_data[i-1]
        
gage_4_data = [round(float(i), 3) for i in gage_4_data]


## POTOMAC LOWER (TO COMPARE WITH RAS WSE)
  
## LEWISETTA
df4_lwt = pd.DataFrame()
df4 = NOAA_forecast(gage_4)
df4_lwt['Stage'] = df4['Stage']*0.3048
idx = df4['Date(EST)']
df4_lwt.index = idx
NOAA_lewisetta = df4_lwt.round(3)
NOAA_lewisetta.to_csv('Lewisetta.csv',sep='\t',encoding='utf-8') 
 
 
#### DAHLGREN
gage = ncd 
df4_dahl2 = pd.DataFrame()
df4_dahl = NOAA_forecast(gage)
del df4_dahl['Flow']
df4_dahl2['Stage'] = df4_dahl['Stage']*0.3048
idx = df4_dahl['Date(EST)']
df4_dahl2.index = idx
NOAA_dahl = df4_dahl2.round(3)
NOAA_dahl.to_csv('Dahlgren.csv',sep='\t',encoding='utf-8') 

 
## POTOMAC UPPER (TO COMPARE WITH RAS WSE) 
 
## WASHINGTON DC
gage = wadc
df4_dc = pd.DataFrame()
df4_wadc = NOAA_forecast(gage)
df4_dc['Stage'] = df4_wadc['Stage']*0.3048
idx = df4_wadc['Date(EST)']
df4_dc.index = idx
NOAA_dc = df4_dc.round(3)
NOAA_dc.to_csv('Washington_DC.csv',sep='\t',encoding='utf-8')
                                                               
#------------------------------------------------------------------------------

#---Headers for unsteady flow file

header_1 = "Flow Title=unsteady_flow\nProgram Version=5.03\nUse Restart= 0\n\
Initial Flow Loc=Anacostia       ,Lower              ,14353.1          \n\
Initial Flow Loc=Potomac         ,Upper              ,203098.2         \n\
Initial Flow Loc=Potomac         ,Lower              ,11980.71         \n\
Boundary Location=Anacostia      ,Lower              ,14353.1      ,    ,                ,                ,                ,\n\
Interval={}MIN\n\
Flow Hydrograph= {}\n".format(dd1,len(gage_1_data))
#Add_line="Interpolate Missing Values=True\n"


header_3 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},{}:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Potomac         ,Upper           ,203098.2,        ,                ,                ,                ,\n\
Interval={}HOUR\n\
Flow Hydrograph= {}\n".format(ras_start,sim_start_hr,dd3,len(gage_3_data))


header_4 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},{}:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Potomac         ,Lower           ,11980.71,        ,                ,                ,                , \n\
Interval={}HOUR\n\
Stage Hydrograph= {}\n".format(ras_start,sim_start_hr, dd4,len(gage_4_data))


footer_1 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},{}:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow= ".format(ras_start,sim_start_hr) 
  

#--Open File, overwrite new file ===> WRITE Unsteady Flow File

os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')

with open(os.path.join(wk_dir,f),'w') as fout:  

     #---Gage 1 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_1_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_1)
   
     j=0
     for i in range(0,nrows):
        # print('row ',i)
        row_values = gage_1_data[j:j+10]
        #row_values[:] = [kk*0.0283 for kk in row_values]   # convert cfs to cms (0.0283)
        row_values = [round(float(jj), 1) for jj in row_values]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(","," ")
        output1 = output.replace("   ", " ")                                       # Replace four white space with one
        fout.write('{}\n'.format(output1))
        j = j+10
        
        
     #---Gage 3 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_3_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_3)
    
     j=0
     for i in range(0,nrows):
        # print('row ',i)
        row_values = gage_3_data[j:j+10]
        #row_values = [kk*0.0283 for kk in row_values]   # convert cfs to cms (0.0283)
        row_values = [round(float(jj), 2) for jj in row_values]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(","," ")
        output3= output.replace("    ", " ")
        fout.write('{}\n'.format(output3))
        j = j+10         
        
        
     #---Gage 4 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_4_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_4)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_4_data[j:j+10]
        #row_values = [kk*0.3048 for kk in row_values]   # convert ft to meter (0.3048)
        row_values = [round(float(jj), 2) for jj in row_values]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(","," ")
        output4= output.replace("   ", " ")
        fout.write('{}\n'.format(output4))
        j = j+10     
        
     fout.write(footer_1)            
     
#------------------------------------------------------------------------------
     
#--Open template, write new file===> Write Plan file
  
# Modify lines in input plan file 
line0 ="Plan Title=Anacostia_Potomac_version1\n" 
line25="Computation Interval=1HOUR\n"
line26="Output Interval=1HOUR\n"
line27="Instantaneous Interval=1HOUR\n"
line28="Mapping Interval=1HOUR\n"
line29="Run HTab= 1\n"                                    
line30="Run UNet= 1\n"
line32="Run PostProcess= 1\n"
line34="Run RASMapper= 1\n"  
line35="UNET Theta= 0.6\n"   # change if tidal signal is not a boundary condition
line40="UNET MxIter= 25\n"   # change if number of iteration is to be changed
 
with open(in_file, 'r') as fin:
    with open(out_file, 'w') as fout:
        for i in range(174):
            line = fin.readline()
            if i!=0 and i != 3 and i !=25 and  i !=26 and i !=27 and i!=28 and i!= 29 and i !=30 and i !=32 and i !=34 and i !=35 and i !=40:
                fout.write(line)
            elif i == 0:
                fout.write(line0)
            elif i == 3:
                fout.write(insert_line)  
            elif i == 25:
                fout.write(line25) 
            elif i == 26:
                fout.write(line26)
            elif i == 27:
                fout.write(line27)
            elif i == 28:
                fout.write(line28)
            elif i == 29:
                fout.write(line29)
            elif i == 30:
                fout.write(line30)
            elif i == 32:
                fout.write(line32)
            elif i == 34:
                fout.write(line34)
            elif i == 35:
                fout.write(line35)
            elif i == 40:
                fout.write(line40)   
            else:
                fout.write(line)
#------------------------------------------------------------------------------                              
                
#--Write project file
                
# for feet: line 510 = English Units\n\ 
                
#---Sections for project file
header_project1="Proj Title=Anacostia_Potomac_version1\n\
Current Plan=p01\n\
Default Exp/Contr=0.3,0.1\n\
SI Units\n\
Geom File=g01\n\
Flow File=u01\n\
Plan File=p01\n\
Y Axis Title=Elevation\n\
X Axis Title(PF)=Main Channel Distance\n\
X Axis Title(XS)=Station\n\
BEGIN DESCRIPTION:\n\
                  \n\
END DESCRIPTION:\n\
DSS Start Date=\n\
DSS Start Time=\n\
DSS End Date=\n\
DSS End Time=\n\
DSS File=dss\n\
DSS Export Filename=\n\
DSS Export Rating Curves= 0 \n\
DSS Export Rating Curve Sorted= 0 \n\
DSS Export Volume Flow Curves= 0 \n\
DXF Filename=\n\
DXF OffsetX= 0 \n\
DXF OffsetY= 0 \n\
DXF ScaleX= 1 \n\
DXF ScaleY= 10 \n\
GIS Export Profiles= 0\n"    


#header_project2 = "\nHRC.QuitRAS\n"

with open(os.path.join(wk_dir,proj ),'w') as fout:  

     fout.write(header_project1)
     #fout.write(header_project2)