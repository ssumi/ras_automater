# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:02:31 2017

@author: Selina

"""

import os
from datetime import datetime, timedelta
import math
import pandas as pd
from datetime import datetime, timedelta
from USGS_Data_Grabber import *

#---set paths, filenames
wk_dir = r'C:\Users\admin\Desktop\REALTIME_RAS'
in_file = os.path.join(wk_dir, r'plan_template.txt')
out_file = os.path.join(wk_dir, r'AutoRAS_v_alpha.p02')
f = 'AutoRAS_v_alpha.u01'                     #---Ouput Unsteady Flow FIle


#--Initialize date, time
end_date = datetime.now()
start_date = end_date - timedelta(days = 2)

y0, m0 ,d0 = start_date.year, start_date.month, start_date.day   # Start date (year, month, day)
y1, m1 ,d1 = end_date.year, end_date.month, end_date.day         # End date

#--Format Datetime objects, create input line (insert_line)
ras_start = start_date.strftime(format = '%d%b%Y')
ras_end = end_date.strftime(format = '%d%b%Y')
insert_line = 'Simulation Date=' + str(ras_start) +',0:00,'+ str(ras_end) + ',24:00\n'


#---Select Gages & Parameter
gage_1 = "01646500"
gage_2 = "01651750"   
gage_3 = "01649500" 

flow  = "00060"
stage = "00065"


#-Get Gage 1 Data
df1 = GrabData(gage_1, y0, m0 ,d0, y1, m1 ,d1,flow)
gage_1_data = list(df1['StreamFlow'])

#-Get Gage 2 Data
df2 = GrabData(gage_2, y0, m0 ,d0, y1, m1 ,d1,stage)
gage_2_data = list(df2['Stage'])

#-Get Gage 3 Data
df1 = GrabData(gage_3, y0, m0 ,d0, y1, m1 ,d1,flow)
gage_3_data = list(df1['StreamFlow'])



#---Check Restart = 0
header_1 = "Flow Title=unsteady_flow\nProgram Version=5.01\nUse Restart= 0\n\
Initial Flow Loc=Potomac         ,Upper           ,187386.9,1810\n\
Initial Flow Loc=Potomac         ,Lower           ,166063.4,8780\n\
Initial Flow Loc=Anacostia       ,Lower           ,17293.75,63\n\
Boundary Location=Potomac        ,Upper           ,187386.9,        ,                ,                ,                ,                \n\
Interval=15MIN\n\
Flow Hydrograph= 2011\n"


header_2 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Potomac         ,Lower           ,8821.243,        ,                ,                ,                ,                \n\
Interval=6MIN\n\
Stage Hydrograph= 5040\n".format(ras_start)  


header_3 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Potomac         ,Lower           ,17293.75,        ,                ,                ,                ,                \n\
Interval=15MIN\n\
Flow Hydrograph= 2016\n".format(ras_start) 


footer_1 ="SS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow= ".format(ras_start) 
  


#--Open File, overwrite new file===> WRITE Unsteady Flow File
with open(os.path.join(wk_dir,f),'w') as fout:    
     data_length = len(gage_1_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_1)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_1_data[j:j+10]
        myout = [str(q).rjust(10) for q in row_values]
        output1 = str(myout).strip('[]').replace("'", "").replace(",","")
        fout.write('{}\n'.format(output1))
        j = j+10    
        
        
     data_length = len(gage_2_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_2)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_2_data[j:j+10]
        myout = [str(q).rjust(10) for q in row_values]
        output2 = str(myout).strip('[]').replace("'", "").replace(",","")
        fout.write('{}\n'.format(output2))
        j = j+10    
        
    
     data_length = len(gage_3_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_3)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_3_data[j:j+10]
        myout = [str(q).rjust(10) for q in row_values]
        output3 = str(myout).strip('[]').replace("'", "").replace(",","")
        fout.write('{}\n'.format(output3))
        j = j+10    
        
     fout.write(footer_1)     




#--Open template, write new file===> WRITE PLAN FILE
with open(in_file, 'r') as fin:
    with open(out_file, 'w') as fout:
        for i in range(174):
            line = fin.readline()
            if i != 3:
                fout.write(line)
            else:
                fout.write(insert_line)   
                