# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:07:08 2017

@author: Selina
"""
import sys
import os
import threading
import subprocess
import sched, time
from datetime import datetime, timedelta

##----- Execute the ras_automater code 

exec(open('./ras_automater_anacostia.py').read())
        
    subprocess.Popen("run_RAS_anacostia.cmd")
    
    # call f() again in 5 seconds
    
    threading.Timer(10, f).start()
