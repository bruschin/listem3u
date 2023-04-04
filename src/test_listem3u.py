#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
  Created on 26 mars 2023

  @author: Nicolas Bruschi

  Tests unitaires de listemp3u.py

  [VERSIONS]
    [2023-03-26] BN V1.0 :  Initialisation
    [2023-03-29] BN V1.1 :  issue 1-listemp3upy-sans-fichier-mp3
"""
import os
import pytest
from listem3u import  FILENAME, VERSION, USAGE, FICS_LISTE, REP_TRAV,\
                      DEFAUT_FICMP3, FICS_LISTE_TAMPON, parametres, action


## GLOBAL

REPERTOIRE = "automation"

# turns all warnings into errors for this module
pytestmark = pytest.mark.filterwarnings("error")

## Fonctions :
##############

def test_version():
  """
    Verifie demande version selon parametres -v,-V,--VERSION,--version
  """
  try:
    assert parametres([f"{FILENAME}","-v"]) == \
      (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","-V"]) == \
      (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","--VERSION"]) == \
      (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","--version"]) == \
      (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,DEFAUT_FICMP3)
    # avec verif fic mp3
    assert parametres([f"{FILENAME}","--version","-m"]) == \
      (0,f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n",REP_TRAV,True)
  except AssertionError as msg1:
    print(f"\n\t>>>>ERREUR test_version :\n{msg1}")

def test_aide():
  """
    Verifie demande aide selon parametres -h,-H,--help,--HELP
  """
  try:
    assert parametres([f"{FILENAME}","-h"]) == \
      (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","-H"]) == \
      (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","--help"]) == \
      (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","--HELP"]) == \
      (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV,DEFAUT_FICMP3)
    # avec verif fic mp3
    assert parametres([f"{FILENAME}","--HELP","-M"]) == \
      (0,f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n",REP_TRAV, True)
  except AssertionError as msg2:
    print(f"\n\t>>>>ERREUR test_aide :\n{msg2}")

def test_aideversion():
  """
    Verifie demande aide + version selon parametres -h + -v
  """
  try:
    assert parametres([f"{FILENAME}","-h","-v"]) == \
      (0,f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}\n",
      REP_TRAV,DEFAUT_FICMP3)
    # avec verif fic mp3
    assert parametres([f"{FILENAME}","-h","-v","--mp3"]) == \
      (0,f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}\n",
      REP_TRAV,True)
  except AssertionError as msg3:
    print(f"\n\t>>>>ERREUR test_aideversion :\n{msg3}")

def test_repertoire():
  """
    Verifie parametres -r,-r,--repertoire,--REPERTOIRE
  """
  try:
    if os.path.exists(REPERTOIRE):
      resultat = 2
      scom = f"\n\t>>>>REPERTOIRE CHOISI: {REPERTOIRE} [OK]\n"
    else:
      resultat = 1
      scom = f"\n\t>>>>REPERTOIRE: {REPERTOIRE} INACESSIBLE.\n"
    assert parametres( [f"{FILENAME}", "-r",f"{REPERTOIRE}"]) == \
      (resultat, scom, f"{REPERTOIRE}", DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","-R",f"{REPERTOIRE}"]) == \
        (resultat, scom, f"{REPERTOIRE}", DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","--repertoire",f"{REPERTOIRE}"]) == \
        (resultat, scom, f"{REPERTOIRE}", DEFAUT_FICMP3)
    assert parametres([f"{FILENAME}","--REPERTOIRE",f"{REPERTOIRE}"]) == \
        (resultat, scom, f"{REPERTOIRE}", DEFAUT_FICMP3)
  except AssertionError as msg4:
    print(f"\n\t>>>>ERREUR test_repertoire :\n{msg4}")

def test_action():
  """
    Verifie fichier existance resultat
  """
  try:
    action(REPERTOIRE , FICS_LISTE_TAMPON, FICS_LISTE, DEFAUT_FICMP3)
    assert os.path.exists(f"{REPERTOIRE}/{FICS_LISTE}") is True
  except AssertionError as msg5:
    print(f"\n\t>>>>ERREUR test_action :\n{msg5}")
