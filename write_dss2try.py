import java.text.SimpleDateFormat as Sdf
import java.lang.System as System
import java.sql.Date as Date
from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.io import *
import datetime
import java
import time
#from time import gmtime, strftime
#from datetime import datetime, date, time

stations = ['Little_Falls', 'Wisconsin_Avenue', 'Washington_DC', 'Alexandria', 'Lewisetta', 'Aquatic_Garden']
xs = ['203098.2','193051.1','186779.5','180705.2','11980.71','10077.79']
reach = ['POTOMAC UPPER','POTOMAC UPPER','POTOMAC UPPER','POTOMAC LOWER','POTOMAC UPPER','ANACOSTIA LOWER']

##-------------------------------------------------------------------------------------------------------------------------------------------##
#                                                                                                                                             #
#                                                         LITTLE FALLS                                                                        #
#                                                                                                                                             #
###############################################################################################################################################

data = list()
#---Read the data from text
file = open("E:/Selina/REALTIME_UPDATED_AND_OLD_FILES_HERE/REALTIME_RAS/Seth_Potomac_Anacostia/VERSION0_MODEL_DEC2017_automate/Wisconsin_Avenue.csv","r") 
hrrr = file.readlines()

#---Date time (same date for all stations)
hrrr2 = [row.split('\t')[0] for row in hrrr]
hec_date = hrrr2[1]      # start
hec_date2 = hrrr2[-1]    # end

start_date = hec_date[0:10]
start_time = hec_date[11:16]

end_date =  hec_date2[0:10]
end_time = hec_date2[11:16]

#s = '2011-03-07'
s = start_date
dt = datetime.date(*map(int, s.split('-')))
dt2 = dt.strftime("%b%Y")
#print(dt.month)
#print(type(dt))
#print(dt)
print(dt2)

#----Water level data
hrrr31 = hrrr[1:-1]
hrrr3 = [row.split('\t')[1] for row in hrrr31]
#hecdate = hrrr2[0].replace('\n','')
#hechour = hrrr2[1].replace('\n','')

lines = hrrr3[:]
for i in lines:
    string = i.replace('\n','')
    number = float(string)
    lst = [float(number)]
    data.append(lst)
    print(data)
data_lst = sum(data, [])
#print(data_lst)

## try to calculate the 4H automatically or get the list of names from dss
try : 
  try :
    myDss = HecDss.open("E:/Selina/REALTIME_UPDATED_AND_OLD_FILES_HERE/REALTIME_RAS/Seth_Potomac_Anacostia/VERSION0_MODEL_DEC2017_automate/OBSRAS.dss")
    tsc = TimeSeriesContainer()
    tsc.fullName = "/POTOMAC UPPER/193051.1/STAGE/01%s/1HOUR/VER1/"%dt2
    start = HecTime(start_date, start_time)
    tsc.interval = 60
    #obs = [0.0,2.0,1.0,4.0,3.0,6.0,5.0,8.0,7.0,9.0,10.0,11.0] 
    obs = data_lst  
    times = []
    for value in obs :
      times.append(start.value())
      start.add(tsc.interval)
    tsc.times = times
    tsc.values = obs
    tsc.numberValues = len(obs)
    tsc.units = "METER"
    tsc.type = "INST-VAL"
    myDss.put(tsc)
    
  except Exception, e :
    MessageBox.showError(' '.join(e.args), "Python Error")
  except java.lang.Exception, e :
    MessageBox.showError(e.getMessage(), "Error")
finally :
  myDss.close()




