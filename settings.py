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
        MsgNumeric(0x0800, 'Température extérieure effective', SHORT, divider=10., unit='°C', idx=22),
        MsgNumeric(0x0B00, 'Température chaudière consigne', USHORT, unit='°C', divider=10.),
        MsgNumeric(0x0B12, 'Température chaudière effective', USHORT, divider=10., unit='°C', idx=8),
        MsgNumeric(0x0896, 'Température ambiante', SHORT, divider=10., unit='°C', idx=4),
        MsgNumeric(0x2306, 'Consigne de température ambiante normale', BYTE, unit='°C'),
        MsgNumeric(0x2307, 'Consigne de température ambiante réduite', BYTE, unit='°C'),
        MsgNumeric(0x2544, 'Température de départ consigne', USHORT, unit='°C', divider=10., idx=26),
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
        MsgNumeric(0x0B16, "Température d'insertion", SHORT, unit='°C', divider=10.),
        MsgNumeric(0x0B1A, 'Primary air shutter', UBYTE, unit='%'),
        MsgNumeric(0x0B1B, 'Secondary air shutter', UBYTE, unit='%'),
        MsgNumeric(0x2323, 'Operation mode (0,1,2,4)', UBYTE),
        MsgNumeric(0x2500, 'Mode actuel [0:veille, 1:marche reduite, 2:marche normale(programmée), 3:marche normale(permanente)]', BYTE),
        MsgNumeric(0x254C, 'Ouverture de la vanne mélangeuse', BYTE, unit='%'),
        MsgNumeric(0x2308, 'Consigne de température régime réception', UBYTE, unit='°C'),
        MsgNumeric(0xa38f, 'Performance actuelle', UBYTE, unit='%', divider=2.),
        MsgNumeric(0x2323, 'Mode de fonctionnement [0: Veille, 1:Eau Chaude, 2:Chauffage et Eau Chaude, 3:Fonctionnement permanent réduit, 4: Fonctionnement permanent normal]'),
        MsgNumeric(0x084B, 'Défaut ?'),
        MsgNumeric(0x0b11, "Mode de fonctionnement [0:Arrêt, 1:Montée température, 2:Action régulation, 4:Phase d'extinction]", idx=23),
        MsgNumeric(0x0B21, 'Défaut actuel', idx=24),  # Idem as 7561 and 756B
        MsgNumeric(0x0B23, 'Entrées numériques 1'),
       ]


# --- Time slots
TISL_2k = [MsgTimeslot(0x2000+i*8+j*128, '2k ' + DAYS[i]) for j in range(4) for i in range(7)]
TISL_3k = [MsgTimeslot(0x3000+i*8+j*128, '3k ' + DAYS[i]) for j in range(4) for i in range(7)]

#TISL_4k = [MsgTimeslot(0x4000+i*8+j*128, '4k ' + DAYS[i]) for j in range(4) for i in range(7)]

ALL_TISL = TISL_2k + TISL_3k


# --- Errors log
ERRL = [MsgErrlog(0x7507+i*9, 'Error {}'.format(i)) for i in range(10)]


# %% Détail des messages de défaut

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
                  'Fermer la porte de cendrier'),
            0xFC:('Brûleur bloqué',
                  'Manque de combustible détecté (température de flamme pas atteinte). Panne de la sonde lambda en cours de fonctionnement',
                  "Contrôler le système d'alimentation, la sonde de température de flamme, la sonde lambda, rajouter des granulés le cas échéant."),
           }


# %% Codage 2 -- circulation chauffage
# --- codages  "A0" à "FB"
CODAGE2_CC = [Codage(0x27a0, 0, (0, 2)),  # avec vitotrol 300A ; reconnaissance automatique
              Codage(0x27a2, 2, (0, 15)),  # avec priorité à la production d'eau chaude sanitaire
              Codage(0x27a3, 2, (-9, 15)),  # si T ext < 1°C pompe de circuit de chauffage "Marche"
              Codage(0x27a4, 0, (0, 1)),  # avec protection contre le gel
              Codage(0x27a5, 5, (0, 15)),  # avec fonction logique de pompe
              Codage(0x27a6, 36, (5, 36)),  # régime économique étendu actif
              Codage(0x27a7, 0, (0, 1)),  # sans fonction économique de la vanne mélangeuse
              Codage(0x27a9, 7, (0, 15)),  # avec temps d'arrêt de la pompe
              Codage(0x27aa, 2, (0, 2)),  # avec réduction de la puissance
              Codage(0x27ab, 20, (0, 200)),  # position minimale de l avanne mélangeuse avec réduction de la puissance de 10%
              Codage(0x27b0, 0, (0, 3)),  # 0 avec commande à distance - 1 marche normale en fonction de la t° extérieure marche réduite avec compensation par la sonde de TA etc..
              Codage(0x27b2, 8, (0, 31)),  # coefficient d'influence de la température ambiante
              Codage(0x27b5, 5, (0, 8)),  # avec commande à distance : avec fonction de logique de pompe en fcn de la température ambiante
              Codage(0x27bb, 1, (0, 1)),  # priorité à la charge réservoir tampon
              Codage(0x27bc, 1, (0, 1)),  # absorption de chaleur forcée en cas de dépassement
              Codage(0x27c3, 125, (10, 255)),  # durée de fonctionnement de la vanne mélangeuse
              Codage(0x27c4, 1, (0, 3)),  # souplesse de l'installation
              Codage(0x27c5, 20, (1, 127)),  # limitation électronique de la température minimale de départ
              Codage(0x27c6, 75, (10, 127)),  # limitation éléctronique de la température maximale
              Codage(0x27c8, 31, (1, 31)),
              Codage(0x27d5, 0, (0, 1)),
              Codage(0x27e1, 1, (0, 2)),  # plage de température pour la consigne de jour de la commande à distance
              Codage(0x27e2, 50, (0, 99)),  # correction de l'affichage de la valeur effective de température ambiante sur la commande à distance
              Codage(0x27f1, 0, (0, 6)),  # fonction séchage de chappe
              Codage(0x27f2, 8, (0, 12)),  # durée limite du mode réception
              Codage(0x27f8, -5, (-61, 10)),  # valeur limite pour le début de l'augmentation de T° de réduit à normale
              Codage(0x27f9, -14, (-60, 10)),  # valeur limite pour la fin de l'augmentation de T° de réduit à normale
              Codage(0x27fa, 20, (0, 50)),  # % pour augmentation de consigne de température lors du passage de T° réduite à T° normale
              Codage(0x27fb, 30, (0, 150)),  # durée du fonctionnement à la T° élevée lors du passage de T° réduite à T° normale (1 pas de réglage = 2mn)
             ]


# %% Codage 2 -- généralités
# --- codages "02" à "05", "08", "8A" à "9F"
CODAGE2_GEN = [Codage(0x778a, 175, (175, 175)),  # ne pas modifier !
               Codage(0x7790, 128, (1, 199)),  # Constante de temps pour le calcul de la modification de la température extérieure 21,3h (1 pas = 10 mn)
               Codage(0x7791, 0, (0, 3)),  # Raccordement aux bornes 1 et 2 de la fiche 143 inactif
               Codage(0x7794, 0, (0, 0)),  # ne pas modifier !
               Codage(0x7795, 0, (0, 1)),  # Sans Vitocom 100
               Codage(0x7796, 0, (0, 0)),  # ne pas modifier !
               Codage(0x7797, 0, (0, 2)),  # avec module de communication LON
               Codage(0x7798, 1, (1, 5)),  # Numéro d'installation Viessmann
               Codage(0x7799, 0, (0, 7)),  # Raccordement aux bornes 2 et 3 de la fiche 143 inactif
               Codage(0x779a, 0, (0, 3)),  # Raccordement aux bornes 1 et 2 de la fiche 143 inactif
               Codage(0x779b, 0, (0, 127)),  # Consigne de température minimale de départ
               Codage(0x779c, 20, (0, 60)),  # Surveillance de l'appareil raccordé au bus LON (min)
               Codage(0x779d, 0, (0, 1)),  # sans extension de fonction 0 à 10V
               Codage(0x779e, 0, (0, 1)),  # 0: sans, 1: avec sonde de température extérieure (reconnaissance automatique)
               Codage(0x779f, 8, (0, 40)),  # différence entre consigne de température de départ et eau de chaudière (K)
              ]


# %% Codage 2 -- chaudière
# --- codages "0A3 à "32"
CODAGE2_CHAUD = [Codage(0x5721, 0, (0, 100)),  # fréquence entretien
                 Codage(0x5722, 0, (0, 255)),  # combustible entretien
                 Codage(0x5723, 0, (0, 24)),  # brûleur entretien
                 Codage(0x5724, 0, (0, 1)),  # mise à 0 du message d'entretiens
                 Codage(0x572f, 100, (70, 130)),  # coefficient correction consommation granulés
                 Codage(0x5730, 10, (5, 30)),  # consigne 30 d'enclenchement pour la réduction de puissance (K)
                 Codage(0x5731, 5, (0, 20)),  # consigne 31 d'enclenchement pour la réduction de puissance (K)
                 Codage(0x5732, 0, (10, 100))]  # amplification de la réduction de puissance


# convert the list into a dictionary
#cCODAGE2_CC = {'{:02X}'.format(u.address%256):u for u in CODAGE2_CC}


# %% Main

if __name__ == "__main__":

    # --- Create a list that contains all messages and group by address
    ALL_MESSAGES = MSGS + ALL_TISL + ERRL + CODAGE2_CC + CODAGE2_CHAUD + CODAGE2_GEN
    ALL_MESSAGES.sort(key=lambda x: x.address)
    TAB = ['{:04X} | {} | {}'.format(elt.address, elt.size, elt.description) for elt in ALL_MESSAGES]
    TAB_ADD = [elt.address for elt in ALL_MESSAGES]
    print '\n'.join(TAB)
