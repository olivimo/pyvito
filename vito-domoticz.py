!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:34:22 2020

@author: olivierm

separate file for domoticz


"""


from telegram import time2char
import settings as se
import vito as vi

    

if __name__ == "__main__":
# --- Open 300 Protocol
    opto = Optolink(se.SER)
    # --- Print and update Messages on Domoticz
    for elt in se.MSGS_DOMOTICZ:
        if opto.read(elt):
            print elt
            if elt.idx != None:
                domoticz(elt.idx, svalue=str(elt.value))

    # --- Print Error log
    print '\nError log:'
    for el in se.ERRL:
        if opto.read(el):
            print el
    # Print and update Errorlog to be improved
    err = se.MsgBoolean(0x084B, 'Défaut ?')
        
    err0_id, err0_date = se.ERRL[0].value
    #print geterrlog()
    #print err0_date
    if opto.read(err):
        if err.value:
            # Error
            print "Défaut chaudière",
            if geterrlog() != err0_date:
                # --- new error
                print " nouvelle erreur"
                seterrlog(err0_date)  # update the errlog variable
                domoticz(25, svalue='{:02X} - {}<br>{}<br>{}'.format(err0_id, *se.DEFAULTS.get(err0_id, ('', '', ''))))
            else:
                # --- no new error
                print " pas de nouvelle erreur"
                domoticz(17, nvalue=4, svalue="Erreur {:02X} ({})".format(err0_id, err0_date))
        else:
            # No Error
            print "Pas de défaut"
            mod = se.MsgNumeric(0x0b11, 'Mode de fonctionnement')
            if opto.read(mod):
                dico_mod = {0:(0, 'Arrêt'),
                            1:(2, 'Montée température'),
                            2:(1, 'Action régulation'),
                            4:(3, "Phase d'extinction")}
                domoticz(17, nvalue=dico_mod.get(mod.value, (2,))[0],
                         svalue=dico_mod.get(mod.value, (2, 'Mode n°{}'.format(mod.value)))[1])
                print dico_mod[mod.value][1]



    opto.close()
