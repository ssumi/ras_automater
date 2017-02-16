# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:54:18 2017

@author: admin
"""

import h5py

hfile = 'AutoRAS_v_alpha.p02.hdf'



with h5py.File(hfile, 'r') as hf:
    root = hf.keys()

    for sub in root:
        print(sub)
        subgrp = hf.get(sub).keys()

        for index, key in enumerate(subgrp):
            print('\t', key)
            subgrp2 = hf[sub].get(key).keys()
            
            for index, key in enumerate(subgrp2):
                print('\t', key)



with h5py.File(hfile, 'r') as hf:
    subgrp = hf['Results']['Unsteady'].get('Output').keys()
    for index, key in enumerate(subgrp):
        print(key)
        
