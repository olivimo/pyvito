#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 09:03:55 2016

@author: olivierm
"""
from telegram import MsgNumeric, MsgAddress, MsgDate, MsgBoolean, MsgErrlog, MsgTimeslot, Codage
from telegram import SHORT, USHORT, UINT, UBYTE, BYTE, DAYS


# %% Constants
SER = '/dev/ttyUSB0'  # Serial
URL = 'http://192.168.1.23:8080'  # Domoticz Server


# %% Vitoligno 300-P Configuration

# --- Messages
MSGS = [MsgAddress(0x00F8, 'ID système'),
        MsgDate(0x088E, 'Date et heure'),
        MsgNumeric(0x5525, 'Température extérieure amortie', SHORT, unit='°C', divider=10.),
        MsgNumeric(0x0800, 'Température extérieure effective', SHORT, divider=10., unit='°C', idx=1),
        MsgNumeric(0x0B00, 'Température chaudière consigne', USHORT, unit='°C', divider=10.),
        MsgNumeric(0x0B12, 'Température chaudière effective', USHORT, divider=10., unit='°C', idx=8),
        MsgNumeric(0x0896, 'Température ambiante', SHORT, divider=10., unit='°C', idx=4),
        MsgNumeric(0x2306, 'Consigne de température ambiante normale', BYTE, unit='°C'),
        MsgNumeric(0x2307, 'Consigne de température ambiante réduite', BYTE, unit='°C'),
        MsgNumeric(0x2544, 'Température de départ consigne', USHORT, unit='°C', divider=10.),
        MsgNumeric(0x2900, 'Température de départ effective', SHORT, divider=10., unit='°C', idx=7),
        MsgNumeric(0x0B1C, 'Vitesse du ventilateur consigne', USHORT, unit='rpm'),
        MsgNumeric(0x0B1E, 'Vitesse du ventilateur effective', USHORT, unit='rpm'),
        MsgNumeric(0x0B14, 'Température de flamme', USHORT, divider=10., unit='°C', idx=19),
        MsgNumeric(0x0B20, 'Puissance de la chaudière', UBYTE, unit='%', idx=3),
        MsgNumeric(0x0B18, 'Teneur en O2', USHORT, divider=10., unit='%', idx=6),
        MsgNumeric(0x08A7, 'Fonctionnement du brûleur', UINT, divider=3600, unit='h', idx=11),
        MsgNumeric(0x088A, "Nombre de démarrages", USHORT, idx=9),
        MsgNumeric(0x08B0, 'Consommation de pellets', UINT, unit='kg', idx=10),
        MsgBoolean(0x2906, 'Pompe chauffage'),
        MsgBoolean(0x2302, 'Régime économique ?'),
        MsgBoolean(0x2303, 'Régime réception ?'),
        MsgNumeric(0x2304, 'Courbe de chauffe : parallèle [-13, 40]', BYTE),
        MsgNumeric(0x2305, 'Courbe de chauffe :pente [0.2, 3.4]', BYTE, divider=10.),
        MsgNumeric(0x0B1A, 'Primary air shutter', UBYTE, unit='%'),
        MsgNumeric(0x0B1B, 'Secondary air shutter', UBYTE, unit='%'),
        MsgBoolean(0x0843, '0843 Multifunktionsausgang HKP M1'),
        MsgNumeric(0x2323, 'Operation mode (0,1,2,4)', UBYTE),
        MsgNumeric(0x2500, 'Mode actuel[0:veille, 1:marche reduite, 2:marche normale(programmée), 3:marche normale(constante)]', BYTE),
        MsgNumeric(0x2300, '0x2300'),
        MsgNumeric(0x2301, '0x2301 mode de fonctionnement ?'),
        MsgNumeric(0x2308, '0x2308'),
        MsgNumeric(0x0847, '0x0847 faute collective'),
        MsgNumeric(0x7500, '0x7500 défaut?'),
        MsgNumeric(0xa38f, '0xa38f équipement de performance réelle'),
       ]


# --- Time slots
TISL = [MsgTimeslot(0x2000+i*8, DAYS[i]) for i in range(7)]


# --- Errors log
ERRL = [MsgErrlog(0x7507+i*9, 'Error {}'.format(i)) for i in range(10)]


# %% Error log
#err = Reading(0x7500, 'Etat chaudière', Number(UBYTE))  # ?
#err = Reading(0x0847, 'Etat chaudière', Number(UBYTE)) # ?


# %% Messages de défaut

# Structure
#  {Adresse: ('comportement', 'cause', 'mesure')}

DEFAULTS = {0x0F:('Marche régulée',
                  'Entretien',
                  "Effectuer l'entretien. Régler le codage '24:0' à l'issue des travaux d'entretien."),
            0xF1:('Brûleur bloqué',
                  "Volet d'air primaire défectueux",
                  "Contrôler la mécanique, l'entraînement et le micro-switch. Supprimer le blocage. Le cas échéant, remplacer les pièces défectueuses."),
            0xF4:('Marche régulée',
                  'Porte de cendrier ouverte',
                  'Fermer la porte de cendrier')
           }


# %% Codage 2 -- circulation chauffage
# --- codages  "A0" à "FB"
CODAGE2_CC = [Codage(0x27a0, 0, (0, 2)),
              Codage(0x27a2, 2, (0, 15)),
              Codage(0x27a3, 2, (-9, 15)),
              Codage(0x27a4, 0, (0, 1)),
              Codage(0x27a5, 5, (0, 15)),
              Codage(0x27a6, 36, (5, 36)),
              Codage(0x27a7, 0, (0, 1)),
              Codage(0x27a9, 7, (0, 15)),
              Codage(0x27aa, 2, (0, 2)),
              Codage(0x27ab, 20, (0, 200)),
              Codage(0x27b0, 0, (0, 3)),
              Codage(0x27b2, 8, (0, 31)),
              Codage(0x27b5, 5, (0, 8)),
              Codage(0x27bb, 1, (0, 1)),
              Codage(0x27bc, 1, (0, 1)),
              Codage(0x27c3, 125, (10, 255)),
              Codage(0x27c4, 1, (0, 3)),
              Codage(0x27c5, 20, (1, 127)),
              Codage(0x27c6, 75, (10, 127)),
              Codage(0x27c8, 31, (1, 31)),
              Codage(0x27d5, 0, (0, 1)),
              Codage(0x27e1, 1, (0, 2)),
              Codage(0x27e2, 50, (0, 99)),
              Codage(0x27f1, 0, (0, 6)),
              Codage(0x27f2, 8, (0, 12)),
              Codage(0x27f8, -5, (-61, 10)),
              Codage(0x27f9, -14, (-60, 10)),
              Codage(0x27fa, 20, (0, 50)),
              Codage(0x27fb, 30, (0, 150)),
             ]


# %% Codage 2 -- généralités
# --- codages "02" à "05", "08", "8A" à "9F"
CODAGE2_GEN = [Codage(0x778a, 175, (175, 175)),  # ne pas modifier !
               Codage(0x7790, 128, (1, 199)),
               Codage(0x7791, 0, (0, 3)),
               Codage(0x7794, 0, (0, 0)),  # ne pas modifier !
               Codage(0x7795, 0, (0, 1)),
               Codage(0x7796, 0, (0, 0)),  # ne pas modifier !
               Codage(0x7797, 0, (0, 2)),
               Codage(0x7799, 0, (0, 7)),
               Codage(0x779a, 0, (0, 3)),
               Codage(0x779b, 0, (0, 127)),
               Codage(0x779c, 20, (0, 60)),
               Codage(0x779d, 0, (0, 1)),
               Codage(0x779e, 0, (0, 1)),
               Codage(0x779f, 8, (0, 40)),
              ]


# %% Codage 2 -- chaudière
# --- codages "0A3 à "32"
CODAGE2_CHAUD = [Codage(0x5721, 0, (0, 100)),  # fréquence entretien
                 Codage(0x5722, 0, (0, 255)),  # combustible entretien
                 Codage(0x5723, 0, (0, 24)),  # brûleur entretien
                 Codage(0x5724, 0, (0, 1)),  #mise à 0 du message d'entretiens
                 Codage(0x572f, 100, (70, 130)),  # coefficient correction consommation
                 Codage(0x5730, 10, (5, 30)),
                 Codage(0x5731, 5, (0, 20)),
                 Codage(0x5732, 0, (10, 100))]


# convert the list into a dictionary
#cCODAGE2_CC = {u.address%256:u for u in CODAGE2_CC}
