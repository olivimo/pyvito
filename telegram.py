#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:08:57 2016

@author: olivierm

"""

from struct import unpack

# %% Functions
def address2str(address):
    """ Function that converts an hex address into str """
    return chr(address//256) + chr(address%256)

def comp_crc(message):
    """ Function that computes the CRC """
    return chr(sum(ord(b) for b in message)%256)

def conv_time(elt):
    """ convert a string into a time """
    if elt == '\xff':
        return '--:--'
    else:
        return '{:02d}:{:02d}'.format(ord(elt)//8, (ord(elt)%8)*10)


# %% Types of numerics
SHORT = ('h', 2)
USHORT = ('H', 2)
BYTE = ('b', 1)
UBYTE = ('B', 1)
UINT = ('I', 4)

DAYS = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

# %% Classes
class Msg(object):
    """ Class that manages messages to be read """
    def __init__(self, address, size, description='', idx=None):
        """ Message initialization
         - address: address of the data
         - size: bytes to be read
         - description: string that describes the data
         - idx: domoticz idx"""

        self.address = address
        self.size = size
        self.description = description
        self.value = None
        self.idx = idx

    def update(self, str2eval):
        """  Method that updates the value of the msg """
        self.value = str2eval

    def __repr__(self):
        if len(self.description) == 0:
            return str(self.value)
        else:
            return self.description + ' : ' + str(self.value)

    @property
    def telegram(self):
        """method that defines the telegram to be sent"""
        tele = b'\x00\x01'
        tele += address2str(self.address)
        tele += chr(self.size)
        tele = chr(len(tele)) + tele
        return tele + comp_crc(tele)


class MsgNumeric(Msg):
    """ Class that manages Numeric messages """
    def __init__(self, address, description='', numtyp=UBYTE, **kwargs):
        super(MsgNumeric, self).__init__(address, numtyp[1], description, kwargs.get('idx', None))
        self.numtyp = numtyp
        self.unit = kwargs.get('unit', '')
        self.divider = kwargs.get('divider', 1)


    def update(self, str2eval):
        """ Method that updates the value of the msg """
        self.value = unpack(self.numtyp[0], str2eval)[0] / self.divider

    def __repr__(self):
        if self.value is None:
            return self.description + ' : ---' + self.unit
        else:
            return self.description + ' : ' + str(self.value) + self.unit


class Codage(MsgNumeric):
    """ Class that manages codage messages """
    def __init__(self, address, default, plage):
        description = '{:02X}:{} {}'.format(address%256, default, list(plage))
        if min(plage) < 0:
            numtyp = BYTE
        else:
            numtyp = UBYTE
        super(Codage, self).__init__(address, description=description, numtyp=numtyp)
        self.plage = plage


class MsgDate(Msg):
    """ Class that manages Date messages """
    def __init__(self, address, description=''):
        super(MsgDate, self).__init__(address, 8, description)

    def update(self, str2eval):
        """ Method that updates the value of the msg """
        stnum = [ord(c) for c in str2eval]
        self.value = DAYS[stnum[4] - 1] + \
        ' {3:02x}/{2:02x}/{0:02x}{1:02x} {5:02x}:{6:02x}:{7:02x}'.format(*stnum)


class MsgErrlog(Msg):
    """ Class that manages Errlog messages """
    def __init__(self, address, description=''):
        super(MsgErrlog, self).__init__(address, 9, description)

    def update(self, str2eval):
        """ Method that updates the value of the msg """
        stnum = [ord(c) for c in str2eval]
        self.value = (stnum[0], '{4:02x}/{3:02x}/{1:02x}{2:02x},{6:02x}:{7:02x}:{8:02x}'.format(*stnum))

    def __repr__(self):
        return self.description + ' : {:02X} - {}'.format(*self.value)


class MsgBoolean(Msg):
    """ Class that manages Boolean messages """
    def __init__(self, address, description=''):
        super(MsgBoolean, self).__init__(address, 1, description)

    def update(self, str2eval):
        val = unpack('B', str2eval)[0]
        self.value = str((val%2) == 1)


class MsgAddress(Msg):
    """ Class that manages Address messages """
    def __init__(self, address, description=''):
        super(MsgAddress, self).__init__(address, 2, description)

    def update(self, str2eval):
        self.value = '0x{:02x}{:02x}'.format(ord(str2eval[0]), ord(str2eval[1]))

class MsgTimeslot(Msg):
    """ Class that manages Timeslot messages """
    def __init__(self, address, description=''):
        super(MsgTimeslot, self).__init__(address, 8, description)


    def update(self, str2eval):
        lis = []
        for (start, stop) in zip(str2eval[::2], str2eval[1::2]):
            lis.append(conv_time(start) + ' ' + conv_time(stop))
        self.value = ' | '.join(lis)

if __name__ == "__main__":
    UNR = MsgNumeric(0x1234, 'température ambiante', USHORT, unit='°C', divider=10.0)
    print UNR
    UNR.update(b'\23\00')
    print UNR
    PLA = MsgTimeslot(0X200, 'lundi')
    PLA.update('\x30\x51\x8b\xa8\xFF\xFF\xFF\xFF')
    print PLA
    DAT = MsgDate(0X4567, 'Date et heure')
    DAT.update('\x20\x15\x04\x11\x06\x19\x21\x26')
    print DAT



