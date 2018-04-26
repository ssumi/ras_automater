# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:07:08 2017

@author: selina
"""

import os
import sys
import time
import requests
import inspect
import pyautogui
import threading
import subprocess
from shutil import copyfile
import win32com.client      #link for the process: https://github.com/solomonvimal/PyFloods/blob/master/HEC_RAS_controller.py
from threading import Timer
from datetime import datetime, timedelta


##-----To clone the github repository (in git cmd)
#cd path to local directory
#git clone copied github repo address


def f():
    
    ##-----Run HEC-RAS repeatedly  
    ## Check directory and change the  directory to the required one
    cwd = os.getcwd()
    print(cwd)
    os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')    
      
    ##-----Execute the ras_automater code 
    exec(open('./ras_automater_updated_potomac_anacostia_forecast_obs.py').read())
       
    ##----Run the cmd file  for compiling in HEC-RAS
    #subprocess.Popen("call_hec_script.cmd") 
    #subprocess.Popen.wait
         
    ##----Run the cmd file  for compiling in HEC-RAS 
    #subprocess.call("call_hec_script.cmd")
    #os.system("taskkill /f /im  Ras.exe")
     
    ##----Control HEC-RAS to run and quit
    RC = win32com.client.Dispatch("RAS503.HECRASCONTROLLER") # HEC-RAS Version 5.0.3
    ras_file = 'E:/Selina/REALTIME_UPDATED_AND_OLD_FILES_HERE/REALTIME_RAS/Seth_Potomac_Anacostia/VERSION0_MODEL_DEC2017_automate/Anacostia_Potomac_version1.prj'
    RC.Project_Open(ras_file)
    RC.Compute_CurrentPlan()
    RC.ShowRas()
    time.sleep(60)
    #MsgBox ('Click Yes to close HEC-RAS')
    #RC.QuitRAS() 
    #inspect.getmembers(RC) 
    os.system("taskkill /f /im  Ras.exe")
                      
    ##----Execute the hdf reader code 
    exec(open('./hdf_reader_loops_final_forecast_obs.py').read())
           
    ##----Remove previous video  
    #os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate\\plots_for_video')
    #os.remove("output.mpeg")
    #os.remove("wse_video.mp4")
    
    ##----Execute the movie maker code
    os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
    exec(open('./movie_maker.py').read())
    
    ##----Convert movie file format to mp4
    os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
    subprocess.Popen("run_movie_converter.cmd")  
    
    ##----Copy video to image folder of repo
    src = 'E:/Selina/REALTIME_UPDATED_AND_OLD_FILES_HERE/REALTIME_RAS/Seth_Potomac_Anacostia/VERSION0_MODEL_DEC2017_automate/plots_for_video/wse_video.mp4'
    dst = 'E:/MasonFloodHazardsResearchLab.github.io/potomac_total_water/images/wse_video.mp4'
    copyfile(src,dst)
   
    ##----Change directory to the repository folder
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')  ## check which folder to push using gitpush
           
    ## Push the figures to github
    subprocess.Popen("git_push.cmd")
    subprocess.Popen("git_push2.cmd") 
    
    ## Check the time 
    t2=datetime.now().strftime(format = '%d-%b-%Y %H:%M:%S')
    print("Model run ended at {}".format(t2))
       
    ## Call f() again in specified seconds
    threading.Timer(21600, f).start() 

f() 



