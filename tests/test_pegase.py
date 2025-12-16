#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Created on 8 avril 2023

@author: Nicolas Bruschi

Tests unitaires de pegase.py

[VERSIONS]
    [2023-04-09] BN V1.0 :  Initialisation
    [2023-04-13] BN V1.1 :  Ajouts tests
    [2025-12-16] CA V1.2.0 : Ajouts tests
'https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-' + \
'expected-exceptions'
"""
import pytest
from src.pegase import  FILENAME, VERSION, USAGE, DUREE_PAUSE_DEFAUT,\
                        parametres, gestion_parametre, \
                        _est_un_badgeage_valide, traitement, \
                        _extracted_from_traitement, _conversion_heures

## GLOBAL

# turns all warnings into errors for this module
pytestmark = pytest.mark.filterwarnings("error")

## Fonctions :
##############

def test_extracted_from_traitement():
	"""
	test de la fonction _extracted_from_traitement
	"""
	try:
		assert _extracted_from_traitement([570],DUREE_PAUSE_DEFAUT) == \
			'depart min : 17H39'
	except AssertionError as msgici:
		assert False , \
			f"\n\t>>>>ERREUR test_extracted_from_traitement :\n{msgici}"

def test_conversion_heures():
	"""
	test de la fonction conversion_heures
	"""
	try:
		assert _conversion_heures(542) == \
			'09H02'
	except AssertionError as msgici:
		assert False , \
			f"\n\t>>>>ERREUR test_conversion_heures :\n{msgici}"

def test_est_badgeage_valide():
	"""
	test de la fonction est_badgeage_valide
	"""
	try:
		assert _est_un_badgeage_valide('9H30',[]) == (0, '', [570])
	except AssertionError as msgici:
		assert False , f"\n\t>>>>ERREUR test_est_badgeage_valide :\n{msgici}"

def test_no_badgeage():
	"""
	test aucun badgage renseigné
	"""
	try:
		assert gestion_parametre('') == \
			(1,f'\n\t>>>> ERREUR: Au moins un badgeage OBLIGATOIRE\n{USAGE}',[])
	except AssertionError as msgici:
		assert False , f"\n\t>>>>ERREUR test_no_badgeage :\n{msgici}"

def test_un_badgeage_vide():
	"""
	test un badgage renseigné = espace
	"""
	try:
		assert gestion_parametre(' ') == \
			(1,f"\n\tNombre de badgeage insuffisant\n{USAGE}",[])
	except AssertionError as msgici:
		assert False , f"\n\t>>>>ERREUR test_un_badgeage_vide :\n{msgici}"

def test_un_separateur_non_conforme():
	"""
	test badgage renseigné = '09h30 +- 11h30'
	"""
	ch_trav = ['09h30', '-+', '11h30']
	try:
		assert gestion_parametre(ch_trav) == (   1, \
			f"\nSeparateur badgeages = {ch_trav[1]} non conforme\n\n{USAGE}", \
			[570])
	except AssertionError as msgici:
		assert False , \
			f"\n\t>>>>ERREUR test_un_separateur_non_conforme :\n{msgici}"

def test_separateur_non_conforme():
	"""
	test badgage renseigné = '09h30 +- 11h30'
	"""
	ch_trav = ['09h30', '+', '11h30']
	try:
		assert gestion_parametre(ch_trav) == (   1, \
			f"\nSeparateur badgeages = {ch_trav[1]} non conforme\n\n{USAGE}", \
			[570])
	except AssertionError as msgici:
		assert False , \
			f"\n\t>>>>ERREUR test_un_separateur_non_conforme :\n{msgici}"

def test_undeux_badgeages():
	"""
	test badgages renseignés = '09h30' ou '09h30 - 11h30'
	"""
	for lst_badges in [[570],[570, 690]]:
		try:
			assert traitement( lst_badges ) == (   0, \
				'depart min : 17H39')
		except AssertionError as msgici:
			assert False , \
				f"\n\t>>>>ERREUR test_undeux_badgeages :\n{msgici}"


def test_version_v():
	"""
	demande version selon parametre -v
	"""
	try:
		assert parametres([f"{FILENAME}","-v"]) == (0,f"{VERSION}")
	except AssertionError as msg1:
		assert False , f"\n\t>>>>ERREUR test_version_v :\n{msg1}"

def test_version_vmaj():
	"""
	Verifie demande version selon parametre -V
	"""
	try:
		assert parametres([f"{FILENAME}","-V"]) == (0,f"{VERSION}")
	except AssertionError as msg1:
		assert False , f"\n\t>>>>ERREUR test_version_V :\n{msg1}"

def test_version_version():
	"""
	Verifie demande version selon parametre --VERSION
	"""
	try:
		assert parametres([f"{FILENAME}","--version"]) == (0,f"{VERSION}")
	except AssertionError as msg1:
		assert False , f"\n\t>>>>ERREUR test_version_version :\n{msg1}"

def test_version_versionmaj():
	"""
	Verifie demande version selon parametre --VERSION
	"""
	try:
		assert parametres([f"{FILENAME}","--VERSION"]) == (0,f"{VERSION}")
	except AssertionError as msg1:
		assert False , f"\n\t>>>>ERREUR test_version_VERSION :\n{msg1}"

def test_version_version_h():
	"""
	Verifie demande version selon parametres --version,-h
	"""
	try:
		assert parametres([f"{FILENAME}","--version","-h"]) == \
			(0,f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}")
	except AssertionError as msg1:
		assert False , f"\n\t>>>>ERREUR test_version_version_h :\n{msg1}"


def test_imprevu_t():
	"""
	Verifie demande imprevue -t
	"""
	try:
		assert parametres([f"{FILENAME}","-t"]) == \
			( 1, f'\n\t>>>> ERREUR: option imprévue.\n{USAGE}')
	except AssertionError as msg2:
		assert False , f"\n\t>>>>ERREUR test_imprevu_t :\n{msg2}"

def test_aide_h():
	"""
	Verifie demande aide selon parametre -h
	"""
	try:
		assert parametres([f"{FILENAME}","-h"]) == \
			(0,f"{USAGE}")
	except AssertionError as msg2:
		assert False , f"\n\t>>>>ERREUR test_aide_h :\n{msg2}"

def test_aide_hmaj():
	"""
	Verifie demande aide selon parametre -H
	"""
	try:
		assert parametres([f"{FILENAME}","-H"]) == (0,f"{USAGE}")
	except AssertionError as msg2:
		assert False , f"\n\t>>>>ERREUR test_aide_H :\n{msg2}"

def test_aide_help():
	"""
	Verifie demande aide selon parametre --help
	"""
	try:
		assert parametres([f"{FILENAME}","--help"]) == (0,f"{USAGE}")
	except AssertionError as msg2:
		assert False , f"\n\t>>>>ERREUR test_aide_help :\n{msg2}"

def test_aide_helpmaj():
	"""
	Verifie demande aide selon parametre --HELP
	"""
	try:
		assert parametres([f"{FILENAME}","--HELP"]) == (0,f"{USAGE}")
	except AssertionError as msg2:
		assert False , f"\n\t>>>>ERREUR test_aide_HELP :\n{msg2}"

def test_aide_helpmaj_mmaj():
	"""
	Verifie demande aide selon parametres --HELP, -M
	"""
	try:
		# avec verif fic mp3
		assert parametres([f"{FILENAME}","--HELP","-M"]) == \
				(1,f'\n\t>>>> ERREUR: option imprévue.\n{USAGE}')
	except AssertionError as msg2:
		assert False , f"\n\t>>>>ERREUR test_aide_HELP_M :\n{msg2}"

def test_aideversion():
	"""
	Verifie demande aide + version selon parametres -h + -v
	"""
	try:
		assert parametres([f"{FILENAME}","-h","-v"]) == \
				(0,f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}")
	except AssertionError as msg3:
		assert False , f"\n\t>>>>ERREUR test_aideversion :\n{msg3}"


def test_un_badgeage():
	"""
	Verifie un badgeage
	"""
	try:
		assert parametres( [f"{FILENAME}", "09:30"]) == (2, "")
	except AssertionError as msg4:
		assert False , f"\n\t>>>>ERREUR test_un_badgeage :\n{msg4}"

def test_traite_un_badgeage_conforme():
	"""
	Verifie un badgeage
	"""
	badges = ["09h30","9h30","09H30","9H30","09:30","9:30"]
	for ch_trav in badges:
		try:
			assert gestion_parametre( [ch_trav]) == (0,"",[570])
		except AssertionError as msg4:
			assert False , \
					f"\n\t>>>>ERREUR test_traite_un_badgeage_conforme :\n{msg4}"

def test_traite_un_badgeage_nonconforme():
	"""
	Verifie un badgeage
	"""
	badges = ["09;30","9-30"]
	for ch_trav in badges:
		try:
			assert gestion_parametre( [ch_trav]) == \
				(1,f"\n\tBadgeage = {ch_trav} non conforme\n\n{USAGE}",[])
		except AssertionError as msg4:
			assert False , \
				f"\n\t>>>>ERREUR test_traite_un_badgeage_nonconforme :\n{msg4}"
