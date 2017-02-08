# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 13:02:31 2017

@author: Selina

"""


import os
from datetime import datetime, timedelta


#--Initialize date, time
end_date = datetime.now()
start_date = end_date - timedelta(days = 2)


#---set paths, filenames
root_dir = r'C:\Users\admin\Desktop\ras_automater\sample_inputs'

in_file = os.path.join(root_dir, r'template.p01')
out_file = os.path.join(root_dir, r'GIS2RAS_ProjectCEIE.p01')


#--Format Datetime objects, create input line (insert_line)
ras_start = start_date.strftime(format = '%d%b%Y')
ras_end = end_date.strftime(format = '%d%b%Y')
insert_line = 'Simulation Date=' + str(ras_start) +',0:00,'+ str(ras_end) + ',24:00\n'

#--Open File, write new file
with open(in_file, 'r') as fin:
    with open(out_file, 'w') as fout:
        for i in range(174):
            line = fin.readline()
            if i != 3:
                fout.write(line)
            else:
                fout.write(insert_line)   
                