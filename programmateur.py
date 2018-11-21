#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:34:22 2018

@author: olivierm

Try to change the Time Slot programmatically

usage
-----
Modify the slots dictionnary and run the program

"""

slots = {
'Lun': '06:00 08:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--',
'Mar': '06:00 08:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--',
'Mer': '07:00 09:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--',
'Jeu': '06:00 08:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--',
'Ven': '06:00 08:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--',
'Sam': '07:00 09:00 | 18:20 22:00 | --:-- --:-- | --:-- --:--',
'Dim': '07:00 09:00 | 18:20 21:30 | --:-- --:-- | --:-- --:--'}

from telegram import time2char
import settings as se
import vito as vi



    
def rev_time(stri):
    """ Function that convert a time into the string msg
    >>> rev_time("06:00 10:10 | 17:30 21:00 | --:-- --:-- | --:-- --:--")
    """

    l = stri.split(' | ')
    res = []
    for elt in l:
        res += [time2char(a) for a in elt.split(' ')]
    return ''.join(res)


# --- Open 300 Protocol
opto = vi.Optolink(se.SER)
    


# --- Write the new time slot
for (ts, jour) in zip(se.ALL_TISL[:7], se.DAYS):
    opto.write(ts.address, rev_time(slots[jour]))




# --- Read and Print the time slot
print '\n         ' + ' | '.join('plage {}'.format(i+1).center(11) for i in range(4))
for ts in se.ALL_TISL:
    if opto.read(ts):
        print ts

# --- Close Protocol
opto.close()


