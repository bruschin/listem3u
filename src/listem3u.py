#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
r"""
	Created on 25 mars 2023

	@author: Nicolas Bruschi

	Exploite fichiers extension m3u dans les sous-répertoires du repertoire de
	travail, pour constituer la liste des fichiers mp3 classés.

	[EN ENTREE]
		[-h |--help : Demande usage] Optionnel
		
		[-m |--mp3 : Verification existence fic mp3] Optionnel. Defaut = False
		[-r |--repertoire] <repertoire de travail>  Optionnel
																								defaut = Repertoire_travail
		[-v |--version : Demande version] Optionnel
		Tous les parametres acceptent casse minuscules/majuscules

	[EN SORTIE]
		0 OK # Constitution dans le repertoire de travail du fichier de sortie
		1 KO

	[VERSIONS]
		[2023-03-25] BN V1.0 :  Initialisation
		[2023-03-26] BN V1.1 :  Filtre les fichiers mp3 listés. Pylint.
																										Tests unitaires
		[2023-03-28] BN V1.2 :  Debug repertoire travail PureWindowsPath
		[2023-03-29] BN V1.3 :  issue 1-listemp3upy-sans-fichier-mp3
		[2023-05-15] BN V1.4 :  introduction 1 parametre OBLIGATOIRE
		[2025-04-04] BN V1.5 :  modification contenus fichiers .m3u
		[2025-06-01] BN V1.6 :  modification contenus fichiers .m3u
		[2025-11-02] BN V1.6.1 : modification nom fichier .m3u
		[2025-11-19] BN V1.9.0 : pipeline github action
		[2025-11-23] BN V1.9.1 : suppression saut ligne après écriture + nb fic
		[2025-12-07] BN V1.9.2 : ajout fct md5
		[2025-12-09] BN V1.9.3 : revision format fichier m3u + sha512
                             # https://fr.wikipedia.org/wiki/M3U
    [2025-12-12] BN V1.9.4 : mise au point
		[2025-12-21] BN V1.9.6 : mise au point pipeline ci/cd

	[REFERENCES]
		https://www.githubstatus.com/
		https://www.sphinx-doc.org/fr/master/index.html
		https://github.com/maltfield/rtd-github-pages/
		https://docs.github.com/en/actions/
		monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge
		https://github.com/marketplace/actions/github-pages-action
		https://github.com/marketplace/actions/sphinx-docs-to-github-pages
		# pour memo : python3 -m http.server
		# Le codage des fichiers m3u est en Latin-1
"""

## Bibliotheques ##

import sys
import getopt
import os
import unicodedata
import fnmatch
import hashlib
from datetime import datetime
from os.path import exists as file_exists

## Variables Globales ##

FILENAME = "listem3u.py"
VERSION = f"\n {FILENAME} version : [2025-12-21 BN V1.9.6]"
SEPARATEUR_REP = "\\"
REP_TRAV = f"P:{SEPARATEUR_REP}Morceaux_choisis"
USAGE = (f"\n  usage: {FILENAME} [OPTIONS]\n"
"  OPTIONS:\n"
"  [-h |--help : Demande usage] Optionnel\n"
"  [-m |--mp3 : Verification existence fic mp3] Optionnel. Defaut = False\n"
"  [-r |--repertoire]   <repertoire de travail> OBLIGATOIRE.\n"
f"                      defaut si absent= {REP_TRAV}\n"
"  [-v |--version : Demande version] Optionnel\n"
"  Tous les parametres acceptent casse minuscules/majuscules.\n")
FICS_LISTE_TAMPON = "liste.m3u"
NOW = datetime.now()
FICS_LISTE = f"000-liste-{NOW.strftime('%d-%m-%Y')}.m3u"
DEFAUT_FICMP3 = False

### Fonctions ###
#################

def hashlib_sha512(fname):
	r"""
		somme de controle sha512 d'un fichier

		[ EN ENTREE ]
			fname (chaine) fichier

		[ EN SORTIE ]
			somme_de_controle (chaine) sha512
	"""
	hash_sha512 = hashlib.sha512()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_sha512.update(chunk)
	return hash_sha512.hexdigest()

def parametres(argv):
	r"""
		Gestion des parametres d'appel = repertoire, help et version

		[ EN ENTREE ]
			argv = Les parametres d'appel du script

		[ EN SORTIE ]
			codeexit (entier) 0, 1 ou 2
			scom (chaine) commentaire
			repertoire_travail (chaine)
			test_presenceficmp3 (boolean)
	"""
	### parametre local
	codeexit = 0
	repertoire_travail = REP_TRAV  # valeur defaut
	oncontinue = 0  # si demande aide = 1 ou version = 10 ou les 2 = 11
	scom = ""  # commentaire si parametre imprevu
	test_presenceficmp3 = DEFAUT_FICMP3 # val defaut
	nb_param = 0

	try:
		# pylint: disable=unused-variable
		options, remainder = \
      getopt.getopt(argv[1:], "hHmMvVr:R:",
										["help", "HELP", "mp3", "MP3",
										"version", "VERSION", "repertoire=",
										"REPERTOIRE=" ] )
		#print(f"debug param : {options},{remainder}\n")

		for opt, arg in options:
			nb_param += 1
			if opt.upper() in ["-H", "--HELP"]:
				oncontinue += 1
			elif opt.upper() in ["-M", "--MP3"]:
				test_presenceficmp3 = True
			elif opt.upper() in ("-R", "--REPERTOIRE"):
				#print(f"debug {arg}")
				oncontinue = 0
				repertoire_travail = arg
			elif opt.upper() in ("-V", "--VERSION"):
				oncontinue += 10
			else:
				### ne devrait pas passer là sans lever une exception
				oncontinue = 2
				scom = f"\n\t>>>>PARAMETRE(S): {opt}, {arg} IMPREVU(S)\n"

		if nb_param == 0:
			scom = f"\n\t>>>>PARAMETRE OBLIGATOIRE MANQUANT:\n{USAGE}\n"
			codeexit = 1
		else:
			match oncontinue:
				case 0:
					if not os.path.exists(repertoire_travail):
						scom = f"\n\t>>>>REPERTOIRE: {repertoire_travail} "\
													"INACESSIBLE.\n"
						codeexit = 1
					else:
						scom = "\n\t>>>>REPERTOIRE CHOISI: "\
								f"{repertoire_travail} [OK]\n"
						codeexit = 2
				case 1:
					scom = f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n"
				# Ne devrait pas passer dans ce cas.
				case 2:
					codeexit = 1
				case 10:
					scom = f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n"
				case 11:
					scom = f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n"\
									f"{VERSION}\n"
				case _:
					scom = "\n\t>>>>Fct parametres : Cas IMPREVU\n"
					codeexit = 1

	except getopt.GetoptError as error:
		scom = f"\n\t>>>> ERREUR: {str(error)}\n{USAGE}"
		codeexit = 1

	return (codeexit, scom, repertoire_travail, test_presenceficmp3)

def action(repert=None, fic_tampon=None, fic=None, testmp3=DEFAUT_FICMP3):
	r"""
		Gestion des parametres d'appel = repertoire, help et version

	[ EN ENTREE ]
		repert (chaine) répertoire de travail
		fic_tampon (chaine) fichier de travail
		fic (chaine) fichier resultat
		testmp3 (boolean) DEFAUT_FICMP3

	[ EN SORTIE ]
		# constitution du fichier de sortie dans le repertoire de travail
		coderetour (entier) 0 OK - 1 KO
		sunecom (chaine) commentaire
	"""
	# pylint: disable=too-many-locals
	### parametre local
	fichiersmp3 = []
	ficfiltre = ""
	ssrep = ""    
	nbrfics = 0
	sunecom = ""

	# initial directory
	#	cwd = os.getcwd()
	#	print(f"DEBUG: {cwd}")

	try:
		os.chdir(repert)
		# menage fichiers si existants
		if file_exists(fic_tampon):
			os.unlink(fic_tampon)
		if file_exists(fic):
			os.unlink(fic)
	except (FileNotFoundError, NotADirectoryError, PermissionError):
		print(f"Something wrong with specified\
				directory {repert}. Exception- ", sys.exc_info())
		return (1, sunecom)

	# trouve tous les fichiers de nom contenant -Playlist.m3u sous ./
	ficm3u = _find("*-Playlist.m3u", './')

	# traite chaque fichier de nom contenant -Playlist.m3u sous repert
	for fichier in ficm3u:
		ssrep = os.path.dirname(fichier).split('/')[-1]
		#print(f"debug action : {ssrep}")
		with open(fichier,"r", encoding="utf-8") as lefic:
			for ligne in lefic:
				if _estexploitable(ligne):
					# filtre sur ligne contenant des blancs...
					ficfiltre = _filtreligne(ligne, ssrep)
					# mention du ssrep...
					miseenforme = f"{ficfiltre} # {ssrep}"
					fichiersmp3.append(miseenforme)
		lefic.close()
	# on classe selon ordre alphabetic des chaines considérées en minuscules
	fichiersmp3.sort(key=str.lower)
	#print(f"debug {fichiersmp3}")
	#ecriture du resultat
	with open(fic,"a",encoding="utf-8") as resultat:
		#print("Debug:\n#EXTM3U\n#PLAYLIST:000\n")
		resultat.write("#EXTM3U\n#PLAYLIST:000")
		for elmt in fichiersmp3:
			miseenforme = elmt.split('#')
			lefich = f"{miseenforme[1].strip()}{SEPARATEUR_REP}"\
     					 f"{miseenforme[0].strip()}"
			resultat.write(f"\n{lefich}")
			nbrfics += 1
			if testmp3 and not file_exists(lefich):
				print(f"\n\t>>>> inexistant : {lefich}")
		# pour la gestion de EOF
		# resultat.write("\n")
	resultat.close()
	sunecom = f"\n\t>>>> {nbrfics} fichiers dans {fic}\n"
	return (0, sunecom)

### Sous Fonctions ###
######################

def _find(pattern, path):
	r"""
		Trouve les fichiers selon pattern sous path

	[ EN ENTREE ]
		pattern (chaine) recherche de fichier
		path (chaine) repertoire

	[ EN SORTIE ]
		result (tableau de chaine) basename + fichier
	"""
	### parametre local
	result = []

	# pylint: disable=unused-variable
	for root, dirs, files in os.walk(path):
		result.extend( os.path.join(root, basename) for \
				basename in files \
						if fnmatch.fnmatch(basename, pattern))
	#print(f"debug _find {result}")
	return result

def _estexploitable(unechaine=None):
	r"""
		Pour ne pas avoir à traiter ensuite les lignes vides ou commentées
	
	[ EN ENTREE ]
		unechaine (chaine) une ligne du fichier m3u

	[ EN SORTIE ]
		booleen True ou False
	"""
	bretour = True
	if unechaine is None or len(unechaine.strip()) == 0:
		bretour = False
	else:
		tamp = unechaine.strip()
		if tamp.startswith('#'):
			bretour = False
			
	return bretour
            

def _filtreligne(unechaine=None, ssrep=None):
	r"""
		Filtre une ligne de fichier m3u, alerte si contient un espace, ou plus
		d'un tiret ou caractère imprévu et renvoie nom du fichier mp3

	[ EN ENTREE ]
		unechaine (chaine) une ligne du fichier m3u
		ssrep (chaine) un repertoire

	[ EN SORTIE ]
		unechaine (chaine)  nom du fichier mp3 retourné
												suppression trailing-space.
												alerte si contient un espace.
	"""
	pattern = unicodedata.normalize('NFKD', unechaine).encode('ascii', 'ignore').decode('ascii')
	#print(f"debug : {pattern}")
	
	### parametre local
	
	if pattern != unechaine:
		print(f"\n\t>>>> Au moins un caractere imprevu : {ssrep} # {unechaine}")
	elif ' ' in unechaine:
		print(f"\n\t>>>> au moins un espace : {ssrep} # {unechaine}")
	elif unechaine.count('-') > 1:
		print(f"\n\t>>>> plus d'1 tiret : {ssrep} # {unechaine}")
	else:
		tamp = unechaine.split('-')
		if tamp[0].capitalize() != tamp[0]:
			print(f"\n\t>>>> majuscules : {ssrep} # {unechaine}")
  
	return unechaine.strip()

### Principal ####
##################

# pragma: no cover
if __name__ == "__main__":
	(coderetour, SCOM, REP, TEST_PRESENCEFICMP3) = parametres(sys.argv)
	if coderetour == 2:
		print(SCOM)
		(coderetour,SCOM) = action( REP, FICS_LISTE_TAMPON, FICS_LISTE, \
																TEST_PRESENCEFICMP3)
	print(SCOM)
	sys.exit(coderetour)
