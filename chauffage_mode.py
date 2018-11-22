#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:34:22 2018

@author: olivierm

Assign Working day or not for scheduling

"""

import sys
from programmateur import rev_time
from telegram import time2char
import settings as se
import vito as vi

slots = {
'off': '06:00 08:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--',
'on' : '07:00 09:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--'}

if len(sys.argv) == 3:
    fichier = open("/home/pi/test.txt", "w")

    # No error when calling this script
    day = sys.argv[1]
    index = se.DAYS.index(day)
    status = sys.argv[2]

    # --- Open 300 Protocol
#    opto = vi.Optolink(se.SER)        

    # --- Write the new time slot        
#    opto.write(se.ALL_TISL[index].address, rev_time(slots[status]))
    fichier.write(str(se.ALL_TISL[index].address))
    fichier.write('\n')
    fichier.write(day + ':' + slots[status])
    fichier.close()

    # --- Close Protocol
#    opto.close()
    