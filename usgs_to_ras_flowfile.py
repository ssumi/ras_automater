# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math
import pandas as pd
from USGS_Data_Grabber import *


wk_dir = 'E:\Selina\CEIE641\Project_CEIE641\Potomac_Project_test1'
f = 'TEST_AUTO.u01'

gage_1 = "01646500"
gage_2 = "01651750"   
gage_3 = "01649500" 


y0, m0 ,d0 = 2017,1, 15                            # Start date (year, month, day)
y1, m1 ,d1 = 2017,1, 17                           # End date


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


header_1 = "Flow Title=Irene2011_Updated\nProgram Version=5.03\nUse Restart= 0\n\
Initial Flow Loc=Potomac         ,Upper           ,187386.9,1810\n\
Initial Flow Loc=Potomac         ,Lower           ,166063.4,8780\n\
Initial Flow Loc=Anacostia       ,Lower           ,17293.75,63\n\
Boundary Location=Potomac        ,Upper           ,187386.9,        ,                ,                ,                ,                \n\
Interval=15MIN\n\
Flow Hydrograph= 2011\n" 


header_2 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time=26AUG2011,0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Potomac         ,Lower           ,8821.243,        ,                ,                ,                ,                \n\
Interval=6MIN\n\
Stage Hydrograph= 5040\n" 


header_3 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time=26AUG2011,0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=Potomac         ,Lower           ,17293.75,        ,                ,                ,                ,                \n\
Interval=15MIN\n\
Flow Hydrograph= 2016\n"


footer_1 ="SS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time=26AUG2011,0:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow= "
  
  
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
