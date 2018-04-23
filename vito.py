#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 11:07:17 2016

@author: olivierm
"""

from time import sleep
import urllib
import json
import logging
import serial
import settings as se
from telegram import comp_crc, address2str
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)  # uncomment this for debug mode


#%% Functions

def str2hexa(message):
    """ Function to show str as hexa string """
    return ' '.join(format(ord(ui), '02x') for ui in message)


def domoticz(idx, nvalue='0', svalue=''):
    """ Function to send message to domoticz virtual sensors """
    url = se.URL
    httpresponse = urllib.urlopen(url + "/json.htm?type=command&param=udevice&idx={}&nvalue={}&svalue={}".format(idx, nvalue, svalue))
    return httpresponse


def geterrlog():
    """ Function to get the value of the domoticz variable """
    url = se.URL
    httpresponse = urllib.urlopen(url + "/json.htm?type=command&param=getuservariable&idx=1")
    data = json.load(httpresponse)
    return data['result'][0]['Value']


def seterrlog(val):
    """ Function to set the value of the domoticz variable """
    url = se.URL
    urllib.urlopen(url + "/json.htm?type=command&param=updateuservariable&vname=lasterror&vtype=2&vvalue={}".format(val))


# %% Optolink Class
class Optolink(object):
    """ Class for communication with optolink """
    def __init__(self, tty='/dev/ttyUSB0'):
        self.ser = serial.Serial(tty, baudrate=4800, bytesize=8, stopbits=2, parity='E')

        # Clean the buffer
        self.ser.flushInput()
        self.ser.flushOutput()
        sleep(1)
        # Close communication if opened
        self.ser.write(chr(0x04))
        # Should catch 0x05
        ret = self.ser.read()
        logging.debug("should catch 0x05 :%s", str2hexa(ret))

        trys = 0
        while trys < 5:
            logging.debug('write 0x16 0x00 0x00')
            self.ser.write(b'\x16\x00\x00')
            ret = self.ser.read()
            logging.debug("should catch 0x06 :%s", str2hexa(ret))
            if  ret == chr(0x06):
                logging.info('Session to Optolink opened')
                break
            trys += 1
            logging.warning('Communication failed (%d/5)', trys)

    def read(self, msg):
        """Read data"""
        # 1. Request
        self.ser.write('\x41')  # telegram start
        self.ser.write(msg.telegram)
        logging.debug(str2hexa(msg.telegram))

        # 2. Read the answer
        try:
            check = self.ser.read(2) == '\x06\x41'  # 0x0641 expected
            size = self.ser.read()  # get the size of the telegram
            telegram = self.ser.read(ord(size))  # read the telegram
            crc = self.ser.read()  # read the crc of the telegram
            logging.debug(str2hexa(size + telegram + crc))

            logging.debug('Received 0x 06 41? ' + str(check))
            assert check
            # check that this a read response
            check = telegram[:2] == '\x01\x01'
            logging.debug('Received 0x 01 01? ' + str(check))
            assert check
            # check this is the right address
            check = telegram[2:4] == address2str(msg.address)
            logging.debug('Return address is the same? ' + str(check))
            assert check
            # check the size of the data
            check = telegram[4] == chr(msg.size)
            logging.debug('Data size is ok? ' + str(check))
            assert check
            # check the crc
            check = comp_crc(size + telegram) == crc
            logging.debug('CRC is ok? ' + str(check))
            assert check

        except AssertionError:
            logging.debug('Value is not updated: failed the check-up')
            return False
        else:
            msg.update(telegram[5:])
            logging.debug('Check-up passed successfully')
            return True

    def write(self, address, data):
        """Write data (under development)
        /!/ experimental use very carefully"""
        # 1. Request
        self.ser.write('\x41')  # telegram start
        tele = b'\x00\x02'  # request for writing
        tele += address2str(address)
        tele += chr(len(data))  # write number of bytes
        tele += data  # data to write
        tele = chr(len(tele)) + tele
        tele += comp_crc(tele)
        self.ser.write(tele)
        logging.debug(str2hexa(tele))

        # 2. Read the answer
        try:
            check = self.ser.read(2) == '\x06\x41'  # 0x0641 expected
            size = self.ser.read()  # get the size of the telegram
            telegram = self.ser.read(ord(size))  # read the telegram
            crc = self.ser.read()  # read the crc of the telegram
            logging.debug(str2hexa(size + telegram + crc))

            logging.debug('Received 0x 06 41? ' + str(check))
            assert check
            # check that this a write response
            check = telegram[:2] == '\x01\x02'
            logging.debug('Received 0x 01 02? ' + str(check))
            assert check
            # check this is the right address
            check = telegram[2:4] == address2str(address)
            logging.debug('Return address is the same? ' + str(check))
            assert check
            # check the size of the data
            check = telegram[4] == chr(len(data))
            logging.debug('Data size is ok? ' + str(check))
            assert check
            # check the crc
            check = comp_crc(size + telegram) == crc
            logging.debug('CRC is ok? ' + str(check))
            assert check

        except AssertionError:
            logging.debug('Value is not updated: failed the check-up')
            return False
        else:
            logging.debug('Check-up passed successfully')
            return True


    def close(self):
        """ Close optolink communication """

        # close protocol 300"""
        # Try to Close Optolink Session
        trys = 0
        while trys < 5:
            self.ser.write(chr(0x04))  # close communication
            ret = self.ser.read()
            if ret == chr(0x06):
                logging.info("[ACK] received")
                break
            elif ret == chr(0x05):
                logging.info("Session to optolink already closed")
                break
            trys += 1
            logging.warning('Communication failed (%d/5)', trys)


# %% Main

if __name__ == "__main__":
    # --- Open 300 Protocol
    opto = Optolink(se.SER)
    # --- Print and update Messages on Domoticz
    for elt in se.MSGS:
        if opto.read(elt):
            print elt
            if elt.idx != None:
                domoticz(elt.idx, svalue=str(elt.value))

    # --- Print the time slot
    print 'Time slot at 0x2000'
    print '\n      ' + ' | '.join('plage {}'.format(i+1).center(11) for i in range(4))
    for ts in se.TISL_2k:
        if opto.read(ts):
            print ts

    print 'Time slot at 0x3000'
    print '\n      ' + ' | '.join('plage {}'.format(i+1).center(11) for i in range(4))
    for ts in se.TISL_3k:
        if opto.read(ts):
            print ts

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

#    new = se.MsgNumeric(0x2304, 'parallele')
#    opto.read(new)
#    print new
#    opto.write(0x2304, 2)  # set the parallel
#    opto.read(new)
#    print new

#    for elt in se.CODAGE2_CC:
#        if opto.read(elt):
#            print elt

    opto.close()
