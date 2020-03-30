#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:34:22 2018

@author: olivierm

Assign Working day or not for scheduling


Preamble
Create a switch in domoticz for every days with the 4 states [off, eco, cnf, cpp]
Define actions for each state (example monday eco) : 
script:///home/pi/pyvito/chauffage_mode.py Lun eco

"""

import sys
from programmateur import rev_time
from telegram import time2char
import settings as se
import vito as vi

slots = {
'off': '--:-- --:-- | --:-- --:-- | --:-- --:-- | --:-- --:--',
'eco': '06:00 08:00 | 17:50 21:30 | --:-- --:-- | --:-- --:--',
'cnf': '07:00 10:00 | 17:50 21:30 | --:-- --:-- | --:-- --:--',
'cpp': '07:00 21:30 | --:-- --:-- | --:-- --:-- | --:-- --:--'
}

if len(sys.argv) == 3:
    
    # No error when calling this script
    day = sys.argv[1]
    index = se.DAYS.index(day)
    status = sys.argv[2]

    # --- Open 300 Protocol
    # fichier = open("/home/pi/pyvito/test.txt", "w")  # for testing purpose
    opto = vi.Optolink(se.SER)        

    # --- Write the new time slot        
    #fichier.write(str(se.ALL_TISL[index].address))   # for testing purpose
    #fichier.write('\n')  # for testing purpose
    #fichier.write(day + ':' + slots[status])  # for testing purpose
    opto.write(se.ALL_TISL[index].address, rev_time(slots[status]))

    # --- Close Protocol
    #fichier.close()  # for testing purpose
    opto.close()
    
