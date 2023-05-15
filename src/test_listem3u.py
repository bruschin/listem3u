#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created on 26 mars 2023

@author: Nicolas Bruschi

Tests unitaires de listemp3u.py

[VERSIONS]
    [2023-03-26] BN V1.0 :  Initialisation
    [2023-03-29] BN V1.1 :  issue 1-listemp3upy-sans-fichier-mp3
    [2023-04-05] BN V1.2 :  3-sonarqube
"""
import os
import pytest
from listem3u import  FILENAME, VERSION, USAGE, FICS_LISTE, REP_TRAV,\
                        DEFAUT_FICMP3, FICS_LISTE_TAMPON, parametres, action, \
                        _filtreligne

## GLOBAL
# initial directory
CWD = os.getcwd()
REPERTOIRE = f"{CWD}/automation"

# turns all warnings into errors for this module
pytestmark = pytest.mark.filterwarnings("error")

## Fonctions :
##############

def test_filtreligne_maj(capsys):
    """
    test les alertes sur les noms de fichiers mp3 lus dans fic m3u
    """
    ssrep = "001"
    unechaine = "Paint_it_Black-The_Rolling_Stones.mp3"
    try:
        chaineretour = _filtreligne( unechaine , ssrep )
        captured = capsys.readouterr()
        assert captured.out == f"\n\t>>>> majuscules : {ssrep} # {unechaine}\n"
        assert chaineretour == unechaine.strip()
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_filtreligne :\n{msg1}"

def test_filtreligne_tiret(capsys):
    """
    test les alertes sur les noms de fichiers mp3 lus dans fic m3u
    """
    ssrep = "001"
    unechaine = "Paint_it_black-The_Rolling-Stones.mp3"
    try:
        chaineretour = _filtreligne( unechaine , ssrep )
        captured = capsys.readouterr()
        assert captured.out == \
            f"\n\t>>>> plus d'1 tiret : {ssrep} # {unechaine}\n"
        assert chaineretour == unechaine.strip()
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_filtreligne :\n{msg1}"

def test_filtreligne_blanc(capsys):
    """
    test les alertes sur les noms de fichiers mp3 lus dans fic m3u
    """
    ssrep = "001"
    unechaine = "Paint_it_black-The Rolling_Stones.mp3"
    try:
        chaineretour = _filtreligne( unechaine , ssrep )
        captured = capsys.readouterr()
        assert captured.out == \
            f"\n\t>>>> au moins un espace : {ssrep} # {unechaine}\n"
        assert chaineretour == unechaine.strip()
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_filtreligne :\n{msg1}"

def test_version_v():
    """
    demande version selon parametre -v
    """
    try:
        assert parametres([f"{FILENAME}","-v"]) == \
        (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_version_v :\n{msg1}"

def test_version_vmaj():
    """
        Verifie demande version selon parametre -V
    """
    try:
        assert parametres([f"{FILENAME}","-V"]) == \
            (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_version_V :\n{msg1}"

def test_version_version():
    """
        Verifie demande version selon parametre --VERSION
    """
    try:
        assert parametres([f"{FILENAME}","--version"]) == \
            (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_version_version :\n{msg1}"

def test_version_versionmaj():
    """
        Verifie demande version selon parametre --VERSION
    """
    try:
        assert parametres([f"{FILENAME}","--VERSION"]) == \
            (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_version_VERSION :\n{msg1}"

def test_version_version_m():
    """
        Verifie demande version selon parametres --version,-m
    """
    try:
        assert parametres([f"{FILENAME}","--version","-m"]) == \
            (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,True)
    except AssertionError as msg1:
        assert False , f"\n\t>>>>ERREUR test_version_version_m :\n{msg1}"


def test_obligatoire_manquant():
    """
        Verifie demande sans argument 
    """
    try:
        assert parametres([f"{FILENAME}"]) == \
            ( 1, f"\n\t>>>>PARAMETRE OBLIGATOIRE MANQUANT:\n{USAGE}\n",
                REP_TRAV, DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_obligatoire_manquant :\n{msg2}"

def test_obligatoire_vide():
    """
        Verifie demande avec argument -r mais rien d'autre 
    """
    try:
        assert parametres([f"{FILENAME}","-r"]) == \
            ( 1, f"\n\t>>>> ERREUR: option -r requires argument\n{USAGE}",
                REP_TRAV, DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_obligatoire_vide :\n{msg2}"

def test_imprevu_t():
    """
        Verifie demande imprevue -t
    """
    try:
        assert parametres([f"{FILENAME}","-t"]) == \
            ( 1, f"\n\t>>>> ERREUR: option -t not recognized\n{USAGE}",
                REP_TRAV, DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_imprevu_t :\n{msg2}"

def test_imprevu_tmaj():
    """
        Verifie demande imprevue -T
    """
    try:
        assert parametres([f"{FILENAME}","-T"]) == \
            ( 1, f"\n\t>>>> ERREUR: option -T not recognized\n{USAGE}",
                REP_TRAV, DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_imprevu_T :\n{msg2}"

def test_imprevu_test():
    """
        Verifie demande imprevue --test
    """
    try:
        assert parametres([f"{FILENAME}","--test"]) == \
            ( 1, f"\n\t>>>> ERREUR: option --test not recognized\n{USAGE}",
                REP_TRAV, DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_imprevu_test :\n{msg2}"

def test_imprevu_testmaj():
    """
        Verifie demande imprevue --TEST
    """
    try:
        assert parametres([f"{FILENAME}","--TEST"]) == \
            ( 1, f"\n\t>>>> ERREUR: option --TEST not recognized\n{USAGE}",
                REP_TRAV, DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_imprevu_TEST :\n{msg2}"

def test_imprevu_testmaj_mmaj():
    """
        Verifie demande imprevue --TEST, -M
    """
    try:
        # avec verif fic mp3
        assert parametres([f"{FILENAME}","--TEST","-M"]) == \
            ( 1, f"\n\t>>>> ERREUR: option --TEST not recognized\n{USAGE}",
                REP_TRAV, DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_imprevu_TEST_M :\n{msg2}"


def test_aide_h():
    """
        Verifie demande aide selon parametre -h
    """
    try:
        assert parametres([f"{FILENAME}","-h"]) == \
            (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_aide_h :\n{msg2}"

def test_aide_hmaj():
    """
        Verifie demande aide selon parametre -H
    """
    try:
        assert parametres([f"{FILENAME}","-H"]) == \
            (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_aide_H :\n{msg2}"

def test_aide_help():
    """
        Verifie demande aide selon parametre --help
    """
    try:
        assert parametres([f"{FILENAME}","--help"]) == \
            (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_aide_help :\n{msg2}"

def test_aide_helpmaj():
    """
        Verifie demande aide selon parametre --HELP
    """
    try:
        assert parametres([f"{FILENAME}","--HELP"]) == \
            (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_aide_HELP :\n{msg2}"

def test_aide_helpmaj_mmaj():
    """
        Verifie demande aide selon parametres --HELP, -M
    """
    try:
        # avec verif fic mp3
        assert parametres([f"{FILENAME}","--HELP","-M"]) == \
            (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV, True)
    except AssertionError as msg2:
        assert False , f"\n\t>>>>ERREUR test_aide_HELP_M :\n{msg2}"

def test_aideversion():
    """
        Verifie demande aide + version selon parametres -h + -v
    """
    try:
        assert parametres([f"{FILENAME}","-h","-v"]) == \
            (0,f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}\n",
            REP_TRAV,DEFAUT_FICMP3)
    except AssertionError as msg3:
        assert False , f"\n\t>>>>ERREUR test_aideversion :\n{msg3}"

def test_aideversion_mp3():
    """
        Verifie demande aide + version selon parametres -h + -v + --mp3
    """
    try:
        # avec verif fic mp3
        assert parametres([f"{FILENAME}","-h","-v","--mp3"]) == \
            (0,f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}\n",
            REP_TRAV,True)
    except AssertionError as msg3:
        assert False , f"\n\t>>>>ERREUR test_aideversion_mp3 :\n{msg3}"


def test_repertoire_r():
    """
        Verifie parametre -r
    """
    for rep in [REPERTOIRE, "nimportequoi"]:
        try:
            if os.path.exists(rep):
                resultat = 2
                scom = f"\n\t>>>>REPERTOIRE CHOISI: {rep} [OK]\n"
            else:
                resultat = 1
                scom = f"\n\t>>>>REPERTOIRE: {rep} INACESSIBLE.\n"
            assert parametres( [f"{FILENAME}", "-r",f"{rep}"]) == \
                (resultat, scom, f"{rep}", DEFAUT_FICMP3)
        except AssertionError as msg4:
            assert False , f"\n\t>>>>ERREUR test_repertoire_r :\n{msg4}"

def test_repertoire_rmaj():
    """
        Verifie parametre -R
    """
    for rep in [REPERTOIRE, "nimportequoi"]:
        try:
            if os.path.exists(rep):
                resultat = 2
                scom = f"\n\t>>>>REPERTOIRE CHOISI: {rep} [OK]\n"
            else:
                resultat = 1
                scom = f"\n\t>>>>REPERTOIRE: {rep} INACESSIBLE.\n"
            assert parametres([f"{FILENAME}","-R",f"{rep}"]) == \
                    (resultat, scom, f"{rep}", DEFAUT_FICMP3)
        except AssertionError as msg4:
            assert False , f"\n\t>>>>ERREUR test_repertoire_R :\n{msg4}"

def test_repertoire_repertoire():
    """
        Verifie parametre --repertoire
    """
    for rep in [REPERTOIRE, "nimportequoi"]:
        try:
            if os.path.exists(rep):
                resultat = 2
                scom = f"\n\t>>>>REPERTOIRE CHOISI: {rep} [OK]\n"
            else:
                resultat = 1
                scom = f"\n\t>>>>REPERTOIRE: {rep} INACESSIBLE.\n"
            assert parametres([f"{FILENAME}","--repertoire",f"{rep}"]) == \
                    (resultat, scom, f"{rep}", DEFAUT_FICMP3)
        except AssertionError as msg4:
            assert False, f"\n\t>>>>ERREUR test_repertoire_repertoire :\n{msg4}"

def test_repertoire_repertoiremaj():
    """
        Verifie parametre --REPERTOIRE
    """
    for rep in [REPERTOIRE, "nimportequoi"]:
        try:
            if os.path.exists(rep):
                resultat = 2
                scom = f"\n\t>>>>REPERTOIRE CHOISI: {rep} [OK]\n"
            else:
                resultat = 1
                scom = f"\n\t>>>>REPERTOIRE: {rep} INACESSIBLE.\n"
            assert parametres([f"{FILENAME}","--REPERTOIRE",f"{rep}"]) == \
                    (resultat, scom, f"{rep}", DEFAUT_FICMP3)
        except AssertionError as msg4:
            assert False, f"\n\t>>>>ERREUR test_repertoire_REPERTOIRE :\n{msg4}"

def test_action():
    """
        Verifie fichier existence du fic resultat selon existence du repertoire
        d'appel
    """
    for rep in [ REPERTOIRE, "nimportequoi"]:
        try:
            iresul = action( rep , FICS_LISTE_TAMPON, FICS_LISTE, \
                                DEFAUT_FICMP3 )
            btest = iresul == 0
            assert os.path.exists(f"{rep}/{FICS_LISTE}") is btest
        except AssertionError as msg5:
            assert False , f"\n\t>>>>ERREUR test_action :\n{msg5}"
