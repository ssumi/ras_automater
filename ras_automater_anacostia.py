# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:02:31 2017

@author: Selina

"""

import os
import math
import pandas as pd
import numpy as np
from USGS_Data_Grabber import *
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


#---set paths, filenames
wk_dir = r'C:\Users\admin\Desktop\REALTIME_RAS\Seth_Anacostia'
in_file = os.path.join(wk_dir, r'plan_template_anacostia.txt')
out_file = os.path.join(wk_dir, r'Anacostia_FEMA.p02')
f = 'Anacostia_FEMA.u01'                                                            # Ouput Unsteady Flow FIle
proj = 'Anacostia_FEMA.prj'


#--Initialize date, time
end_date = datetime.now()
start_date = end_date - timedelta(days = 2)


y0, m0 ,d0 = start_date.year, start_date.month, start_date.day                      # Start date (year, month, day)
y1, m1 ,d1 = end_date.year, end_date.month, end_date.day                            # End date


#--Format Datetime objects, create input line (insert_line)
ras_start = start_date.strftime(format = '%d%b%Y')
ras_end = end_date.strftime(format = '%d%b%Y')


#--Fix the simulation time window
sim_time = datetime.now()-timedelta(minutes = 65)                                   # (any) minutes before now to give the time to donload data
sim_hr =  '%02d' % sim_time.hour                                                    # simulation hour in 00:00 format
sim_min = '%02d' % sim_time.minute                                                  # simulation minute in 00:00 format
ras_end_updated = sim_time.strftime(format = '%d%b%Y')                              # simulation end date based on date of last available data 
# simulation date, hour, minute
insert_line = 'Simulation Date=' + str(ras_start) +',0:00,'+ str(ras_end_updated) + ',{}:{}\n'.format(sim_hr, sim_min)
                                                                                             

#---Select gages & parameter
gage_1 = "01649500"                                                                 # Northeast Anacostia 
gage_2 = "01651750"                                                                 # Lower Anacostia 
gage_3 = "01651000"                                                                 # NW Anacostia


flow  = "00060"
stage = "00065"

#------------------------------------------------------------------------------

#---Get Gage 1 Data (df1 for StreamFlow)
df1 = GrabData(gage_1, y0, m0 ,d0, y1, m1 ,d1,flow)
#df1.count()                                                                        # count total data available


#---Get the time interval of data
df1['deltaT'] = df1.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd1=int(df1["deltaT"].iloc[-1])                                                     # value of the time interval (uniform in this data set)

#--Handling the missing values in usgs gage  data

index_time = datetime.now()-timedelta(minutes = 50) 
start_index = start_date.strftime(format = '%Y-%m-%d 00:00:00')                     # start date for the corrected time index including missing data date
end_index = index_time.strftime(format = '%Y-%m-%d %H:%M:%S')                       # end date for the index with hr,min and sec
idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd1))               # indexing the time for date interval
df1 = df1.reindex(idx, fill_value="")                                               # fill the missing places of indexed gage data with empty space

######################################################                                                                       
#df1.isnull().count()                                                               # count including  missing data                                              
#count_NULL1=df1.interpolate().count()
#df1=df1.interpolate(method='time')                                                 #interpolate using any method
######################################################

#---Get the streamflow data from whole data frame                                                                        
gage_1_data = list(df1['StreamFlow'])        
print(df1.iloc[-1])                                                                 # Check the last date and time
#df1.index                                                                          # Check index of the dataframe
#df1.plot()                                                                         # Plot gage data

                                                                             
#------------------------------------------------------------------------------

#---Get Gage 2 Data (df2 for Stage)
df2 = GrabData(gage_2, y0, m0 ,d0, y1, m1 ,d1,stage)

###############################################################################
#-----what method to use for interpolate data for missing values//RESTART file-
###############################################################################

#---Get the time interval of data
df2['deltaT'] = df2.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd2=int(df2["deltaT"].iloc[-1])                                                     # value of the time interval (uniform in this data set)

#--Handling the missing values in usgs gage data
idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd2))               # indexing the time for date interval
df2 = df2.reindex(idx, fill_value="") 
#count_NULL2=df2.interpolate().count()
#df2=df2.interpolate(method='time')

#---Get the stage data from whole data frame     
gage_2_data = list(df2['Stage'])
print(df2.iloc[-1])
#df2.plot()                                                                         # Plot gage data


#------------------------------------------------------------------------------

#---Get Gage 3 Data (df3 for Stage)
df3 = GrabData(gage_3, y0, m0 ,d0, y1, m1 ,d1,flow)

#---Get the time interval of data
df3['deltaT'] = df3.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd3=int(df3["deltaT"].iloc[-1])                                                     # value of the time interval (uniform in this data set)

#--Handling the missing values in usgs gage data
idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd3))               # indexing the time for date interval
df3 = df3.reindex(idx, fill_value="")
#count_NULL3=df3.interpolate().count()
#df3=df3.interpolate(method='time')

#---Get the flow data from whole data frame 
gage_3_data = list(df3['StreamFlow'])
print(df3.iloc[-1])
#df3.plot()

#------------------------------------------------------------------------------

#---Headers for unsteady flow file

header_1 = "Flow Title=unsteady_flow\nProgram Version=5.03\nUse Restart= 0\n\
Initial Flow Loc=Anacostia       ,Northeast          ,1.99   ,32\n\
Initial Flow Loc=Anacostia       ,Lower              ,8.27   ,48\n\
Initial Flow Loc=NW Anacostia    ,NW                 ,1.75   ,16\n\
Boundary Location=Anacostia      ,Northeast           ,1.99   ,        ,                ,                ,                ,\n\
Interval={}MIN\n\
Flow Hydrograph= {}\n".format(dd1,len(gage_1_data))
#Add_line="Interpolate Missing Values=True\n"


header_2 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Anacostia         ,Lower           ,8.27,        ,                ,                ,                ,\n\
Interval={}MIN\n\
Stage Hydrograph= {}\n".format(ras_start,dd2,len(gage_2_data))


header_3 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Anacostia         ,Lower           ,0.44,        ,                ,                ,                ,\n\
Interval={}MIN\n\
Stage Hydrograph= {}\n".format(ras_start,dd2,len(gage_2_data))


header_4 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=NW Anacostia         ,NW           ,1.75,        ,                ,                ,                ,\n\
Interval={}MIN\n\
Flow Hydrograph= {}\n".format(ras_start,dd3,len(gage_3_data))


footer_1 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow= ".format(ras_start) 
  

#--Open File, overwrite new file===> WRITE Unsteady Flow File

with open(os.path.join(wk_dir,f),'w') as fout:  

    #---Gage 1 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_1_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_1)
   
     j=0
     for i in range(0,nrows):
        # print('row ',i)
        row_values = gage_1_data[j:j+10]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'","").replace(","," ")
        output1 = output.replace("    ", "  ")                                       # Replace four white space with one
        fout.write('{}\n'.format(output1))
        j = j+10    
        
    #---Gage 2 formatted unsteady flow data for HEC-RAS   
     data_length = len(gage_2_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_2)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_2_data[j:j+10]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(", ","  ")
        output2= output.replace("   ", " ")
        fout.write('{}\n'.format(output2))                                           ###Anacostia Lower at 8.27
        j = j+10
        
                   
    #---Again Gage 2 formatted unsteady flow data for HEC-RAS   
     fout.write(header_3)
    
     j=0
     for i in range(0,nrows):
         
        #print('row ',i)
        row_values = gage_2_data[j:j+10]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(", ","  ")
        output2= output.replace("   ", " ")
        fout.write('{}\n'.format(output2))                                          ###Anacostia Lower at 0.44
        j = j+10 
        
    #---Gage 3 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_3_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_4)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_3_data[j:j+10]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'","").replace(","," ")
        output3= output.replace("    ", "  ")
        fout.write('{}\n'.format(output3))
        j = j+10     
        
     fout.write(footer_1)   
     
#------------------------------------------------------------------------------
     
#--Open template, write new file===> Write Plan file
  
# Modify lines in input plan file 
line0 ="Plan Title=Anacostia_FEMA\n" 
line25="Computation Interval=6HOUR\n"
line26="Output Interval=6HOUR\n"
line27="Instantaneous Interval=6HOUR\n"
line28="Mapping Interval=6HOUR\n"
line29="Run HTab= 1\n"                                    
line30="Run UNet= 1\n"
line32="Run PostProcess= 1\n"
line34="Run RASMapper= 1\n"  
 
with open(in_file, 'r') as fin:
    with open(out_file, 'w') as fout:
        for i in range(174):
            line = fin.readline()
            if i!=0 and i != 3 and i !=25 and  i !=26 and i !=27 and i!=28 and i!= 29 and i !=30 and i !=32 and i !=34:
                fout.write(line)
            elif i == 0:
                fout.write(line0)
            elif i == 3:
                fout.write(insert_line)  
            elif i == 25:
                fout.write(line29) 
            elif i == 26:
                fout.write(line29)
            elif i == 27:
                fout.write(line29)
            elif i == 28:
                fout.write(line29)
            elif i == 29:
                fout.write(line29)
            elif i == 30:
                fout.write(line30)
            elif i == 32:
                fout.write(line32)
            elif i == 34:
                fout.write(line34)
            else:
                fout.write(line)
#------------------------------------------------------------------------------                              
                
#--Write project file
            
#---Sections for project file

header_project1="Proj Title=Anacostia_FEMA\n\
Current Plan=p02\n\
Default Exp/Contr=0.3,0.1\n\
English Units\n\
Geom File=g01\n\
Flow File=u01\n\
Plan File=p02\n\
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


with open(os.path.join(wk_dir,proj ),'w') as fout:  

     fout.write(header_project1)