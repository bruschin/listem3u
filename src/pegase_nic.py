#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# pylint: disable=too-many-branches
"""
	Created on 14 mars 2023

	@author: Nicolas Bruschi

	Calcule l'heure de départ minimale theorique pour effectuer obligation de
	7h24 de travail effectif d'apres renseignement de 1 ou 3 badgeages de type
	xxhmm exemple 9:24 ou 09h24 ou 13H56 (le h ou : central accepte la casse
	min/maj). Pour renseigner une séquence de 3 badgeage copie/colle sur
	pegaseweb:  09:33 - 12:09 - 12:35

	Nota bene : le systeme pivot par défaut pris en compte est celui de 37h/5j
	pour adapter ce systeme pivot à son cas , il convient de modifier en dur
	dans ce script la valeur de la variable globale DUREE_JOUR. Exemple:
	38h30 / 5j : (38*60 +30)/5 = 462 = 7*60 + 42 = Obligation quotidienne 7h42.

	[ EN ENTREE ]
		1 ou 3 arguments de type chaine = xxhmm ou xHmm
		exemple 9h24 ou 09:24 ou 13H56 (:,h central accepte la casse min/maj)
		Si un seul arg on appliquera automatiquement une pause midi obligatoire
		de 45 minutes
		Si 3 arg, séparé par (-, ou /) la duree entre arg 2 et arg 3 est la
		duree de la pause meridienne ne pouvant etre inf a 45 minutes.
	[ EN SORTIE ]
		0   OK => Affichage de l'heure du depart calcule ex: DEPART : 17H19
		1   KO Arguments appel incorrects ou en nombre incorrect.
				=> Affichage raison pb.

	[VERSIONS]
		[2023-03-14] BN V1.0 : Initialisation
		[2023-04-09] BN V1.1 : Test unitaires + gestion param aide + version
		[2023-04-13] BN V1.2 : Test unitaires + corretion bug _conversion_heures 
													 %02d prise en compte 1 ou 3 badgeages => 1 ou 2 ou 3.
		[2024-09-11] BN V1.3 : Ajout calcul systeme pivot autre que 37h5j
"""

## Bibliotheques ##

import sys
import getopt

# VARIABLES GLOBALES :

FILENAME = "pegase_nic.py"
VERSION = f"  {FILENAME}: [2024-09-11] BN V1.3\n"
USAGE = (f"  usage: {FILENAME} [OPTIONS]\n" +\
"  OPTIONS:\n"
"  [09:31 - 12h00 - 12H38] 1 ou 3 badgeage(s) OBLIGATOIRE(S)\n" +\
"  [-h |--help : Demande usage] Optionnel\n" +\
"  [-v |--version : Demande version] Optionnel\n"
"  Tous les parametres acceptent casse minuscules/majuscules.\n")
DUREE_JOUR = 444  # 7h24 convertis en minutes (37h sur 5 j = 7h24 par jour)
#DUREE_JOUR = 462 # Pivot 38h30 5j => 462 minutes = 7h42 par jour
DUREE_PAUSE_DEFAUT = 45
SEPARHM = ["H",":"]
SEPARBADGE = ["-","/"]

## Fonctions :
##############

def parametres(argv):
	"""_
	Gestion des parametres d'appel = help et version

	[ EN ENTREE ]
		argv = Les parametres d'appel du script

	[ EN SORTIE ]
		coderetour (int)    0 ou 1 ou 2
			0       OK  =>  Affichage : aide usage ou version
			1       KO  =>  arguments appel incorrects ou en nombre
											incorrect.
			2           =>  parametres ne contiennent pas de
											demande d'aide ou de version on sort et
											continue
		scom (chaine)			commentaire
									=>  Affichage raison Pb
	"""
	scom = ""
	coderetour = 2
	filtrevolonte = 0
	try:
		# pylint: disable=unused-variable
		options, _ = getopt.getopt( argv[1:], "hHvV", [	"help","HELP",
																										"version", "VERSION"])

		for opt, arg in options:
			if opt in ["-h", "-H", "--help", "--HELP"]:
				filtrevolonte += 1
			elif opt in ("-v", "-V", "--version", "--VERSION"):
				filtrevolonte += 10

		# selon cas ! attention code valable seulement en python 3.10
		match filtrevolonte:
			case 0:
				# tout est ok
				coderetour = 2
			case 1: # help
				scom = f"{USAGE}"
				coderetour = 0
			case 10: # version
				scom = f"{VERSION}"
				coderetour = 0
			case 11: # help + version
				scom = f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}"
				coderetour = 0
			# ne devrait pas passer ici sans lever une exception
			case _:
				scom = "\n\t>>>>Fct parametres : Cas IMPREVU\n"
				coderetour = 1
	except getopt.GetoptError:
		scom = f'\n\t>>>> ERREUR: option imprévue.\n{USAGE}'
		coderetour = 1

	return coderetour, scom

def gestion_parametre(*args):
	"""

	Gestion des parametres d'appel

	[ EN ENTREE ]
			*args = Tous les parametres d'appel du script

	[ EN SORTIE ]
			bretour (int)  0 ou 1
			scom (chaine) commentaire
			minutesici (tableau d'entier) des minutes calculées.
	"""
	# Variables locales:
	####################
	bretour = 0
	scom = ""
	minutesici = []

	if len(args[0]) == 0:
		scom = f'\n\t>>>> ERREUR: Au moins un badgeage OBLIGATOIRE\n{USAGE}'
		bretour = 1
	else:
		for chaine in args[0]:
			# controle au moins un param non vide
			# on passe la chaine en majuscule et on supprime tous les espaces
			ch_trav = chaine.upper().replace(" ","")
			longueur = len(ch_trav)

			match longueur:
				case 0:
					scom = f"\n\tNombre de badgeage insuffisant\n{USAGE}"
					bretour = 1
				case 1:
					separateur = next((sep for sep in SEPARBADGE if ch_trav == sep), "")
					if separateur == "":
						scom = f"\nSeparateur badgeages = {ch_trav}" + \
							f" non conforme\n\n{USAGE}"
						bretour = 1
						break
				case 4|5:
					# la liste non vide est-elle un badgeage ?
					bretour, scom, minutesici = \
					_est_un_badgeage_valide(ch_trav, minutesici)
					if bretour == 1:
						break
				case _:
					# imprevu
					scom = f"\nSeparateur badgeages = {ch_trav}" + \
								 f" non conforme\n\n{USAGE}"
					bretour = 1
					break

	return bretour, scom, minutesici

def traitement(tabminutes):
	"""
	affichage finale selon nombre de badgeages recupérés.

	[ EN ENTREE ]
		tabminutes (tableau d'entier)

	[ EN SORTIE ]
		bret = 0 OK ou 1 KO
		scom (chaine)
	"""
	bret = 0
	scom = ""
	uncompteur = len(tabminutes)

	match uncompteur:
		case 3:
			pause = max((tabminutes[2] - tabminutes[1]), DUREE_PAUSE_DEFAUT)
			scom = _extracted_from_traitement(tabminutes, pause)
		case 1|2:
			scom = _extracted_from_traitement(tabminutes, DUREE_PAUSE_DEFAUT)
		case _:
			scom =  f'\n\t>>>> ERREUR: Nombre badgeage {uncompteur}' +\
							f' imprevu\n\n{USAGE}'
			bret = 1

	return bret, scom

### Sous Fonctions ###
######################

def _est_un_badgeage_valide(ch_trav, conversion):
	"""
	la liste non vide traitée est-elle un badgeage ?

	[ EN ENTREE ]
		ch_trav (chaine) badgeage ?
		conversion (tableau d'entier) badgeage hh:mm converti en minute

	[ EN SORTIE ]
		ret (int) 0 ou 1
		som (chaine) commentaire
		conversion (tableau d'entier) avec ce badgeage en plus
	"""
	# la chaine de la liste de bonne longueur est-elle un badgeage ?
	# separateur entre h et minute
	ret = 0
	scom = ""
	separateur = ""
	separateur = next((sep for sep in SEPARHM if sep in ch_trav), "")
	if separateur == "":
		scom = f"\n\tBadgeage = {ch_trav} non conforme\n\n{USAGE}"
		ret = 1
	else:
		sheure,sminute = ch_trav.split(separateur)
		try:
			sheure = int(sheure, base=10)
			sminute = int(sminute, base=10)
			conversion.append(_conversion_minutes(sheure, sminute))
		except ValueError:
			scom = f"\n\tBadgeage = {ch_trav} non conforme\n"
			ret = 1

	return ret, scom, conversion

def _conversion_minutes(desheures, desminutes):
	"""_
	Conversion heures et minutes passe en appel (de type hh et mm)
	en un entier = minutes

	[ EN ENTREE ]
		desheures (entier) 09 converti en 9
		desminutes (entier)

	[ EN SORTIE ]
		minutes : entier exemple 9*60 + 15 = 555

	"""
	return (60 * desheures) + desminutes

def _conversion_heures(desminutes):
	"""
	Conversion des minutes en xHmm ( 542 -> 09h02 et non pas 9H2)

	[ EN ENTREE ]
		desminutes (entier)

	[ EN SORTIE ]
		ch_conv_retour (chaine) formatee
	"""
	# Variables locales
	lesheures = 0
	lesminutes = 0

	lesheures = desminutes // 60
	lesminutes = desminutes % 60
	# test zfill et rjust
	return f"{str(lesheures).zfill(2)}H{str(lesminutes).rjust(2, '0')}"

def _extracted_from_traitement(tabminutes, pause):
	"""
	extraction de code dupliqué dans la fonction traitement

	[ EN ENTREE ]
		tabminutes (tableau d'entier)

	[ EN SORTIE ]
		ch_conv_retour (chaine) formatee
	"""
	soir = tabminutes[0] + pause + DUREE_JOUR
	depart = _conversion_heures(soir)

	return f"depart : {depart}"

### Principal ###
#################

if __name__ == "__main__":
	retour, commentaire = parametres(sys.argv)

	if retour < 2:
		print(commentaire)
		sys.exit(retour)

	retour, commentaire, minutes = gestion_parametre(sys.argv[1:])

	if retour != 1:
		retour, commentaire = traitement(minutes)

	print(commentaire)
	sys.exit(retour)
