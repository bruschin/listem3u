#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
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

  [REFERENCES]
    https://www.githubstatus.com/
    https://www.sphinx-doc.org/fr/master/index.html
    https://github.com/maltfield/rtd-github-pages/
    https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/
    adding-a-workflow-status-badge
    https://github.com/marketplace/actions/github-pages-action
    https://github.com/marketplace/actions/sphinx-docs-to-github-pages
    # pour memo : python3 -m http.server
"""

## Bibliotheques ##

import sys
import getopt
import os
import fnmatch
from datetime import datetime
from os.path import exists as file_exists

## Variables Globales ##

FILENAME = "listem3u.py"
VERSION = f"\n {FILENAME} version : [2023-03-29 BN V1.3]"
REP_TRAV = "P:\\Morceaux_choisis"
USAGE = (f"\n  usage: {FILENAME} [OPTIONS]\n"
"  OPTIONS:\n"
"  [-h |--help : Demande usage] Optionnel\n"
"  [-m |--mp3 : Verification existence fic mp3] Optionnel. Defaut = False\n"
"  [-r |--repertoire] <repertoire de travail> Optionnel\n"
f"                                             defaut = {REP_TRAV}\n"
"  [-v |--version : Demande version] Optionnel\n"
"  Tous les parametres acceptent casse minuscules/majuscules.\n")
FICS_LISTE_TAMPON = "liste.m3u"
NOW = datetime.now()
FICS_LISTE = f"liste-{NOW.strftime('%d-%m-%Y')}.m3u"
DEFAUT_FICMP3 = False

## Fonctions :
##############

def parametres(argv):
  """ Gestion des parametres d'appel = repertoire, help et version

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
  try:
    # pylint: disable=unused-variable
    options, remainder = getopt.getopt( argv[1:], "hHmMvVr:R:",
                                        ["help", "HELP", "mp3", "MP3",
                                        "version", "VERSION", "repertoire=",
                                        "REPERTOIRE=" ] )
    #print(f"debug param : {options},{remainder}\n")

    for opt, arg in options:
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
        oncontinue = 2
        scom += f"\n\t>>>>PARAMETRE(S): {opt}, {arg} IMPREVU(S)\n"
    #print(f"debug param : {opt.upper()},{arg}\n")
    match oncontinue:
      case 0:
        #print(f"debug chemin : {pathlib.PureWindowsPath(repertoire_travail)}")
        if not os.path.exists(repertoire_travail):
          scom = f"\n\t>>>>REPERTOIRE: {repertoire_travail} INACESSIBLE.\n"
          codeexit = 1
        else:
          scom = f"\n\t>>>>REPERTOIRE CHOISI: {repertoire_travail} [OK]\n"
          codeexit = 2
      case 1:
        scom = f"\n\t>>>>DEMANDE AIDE:\n{USAGE}\n"
      case 2:
        codeexit = 1
      case 10:
        scom = f"\n\t>>>>DEMANDE VERSION:\n{VERSION}\n"
      case 11:
        scom = f"\n\t>>>>DEMANDE AIDE + VERSION:\n{USAGE}\n{VERSION}\n"

  except getopt.GetoptError as error:
    scom = f"\n\t>>>> ERREUR: {str(error)}\n"
    scom += f"{USAGE}"
    codeexit = 1

  return (codeexit, scom, repertoire_travail, test_presenceficmp3)

def find(pattern, path):
  """
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
  #print(f"debug find {result}")
  return result

def action(repert=None, fic_tampon=None, fic=None, testmp3=DEFAUT_FICMP3):
  """_
    Gestion des parametres d'appel = repertoire, help et version

  [ EN ENTREE ]
      repert (chaine) répertoire de travail
      fic_tampon (chaine) fichier de travail
      fic (chaine) fichier resultat
      testmp3 (boolean) DEFAUT_FICMP3

  [ EN SORTIE ]
      constitution du fichier de sortie dans le repertoire de travail
  """
  ### parametre local
  fichiersmp3 = []
  ficfiltre = ""
  ssrep = ""

  # initial directory
  #cwd = os.getcwd()

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
    sys.exit(1)

  # trouve tous les fichiers de nom contenant -Playlist.m3u sous ./
  ficm3u = find("*-Playlist.m3u", './')

  # traite chaque fichier de nom contenant -Playlist.m3u sous repert
  for fichier in ficm3u:
    ssrep = os.path.dirname(fichier).split('/')[-1]
    #print(f"debug action : {ssrep}")
    with open(fichier,"r", encoding="utf-8") as lefic:
      for ligne in lefic:
        # TODO: faire un filtre sur ligne contenant des blancs...
        ficfiltre = filtreligne(ligne, ssrep)
        # TODO: ajouter mention du ssrep...
        miseenforme = f"{ficfiltre} # {ssrep}"
        fichiersmp3.append(miseenforme)
    lefic.close()
  # on classe selon ordre alphabetic des chaines considérées en minuscules
  fichiersmp3.sort(key=str.lower)
  #print(f"debug {fichiersmp3}")
  #ecriture du resultat
  with open(fic,"a",encoding="utf-8") as resultat:
    for elmt in fichiersmp3:
      miseenforme = elmt.split('#')
      lefich = f"{miseenforme[1].strip()}/{miseenforme[0].strip()}"
      resultat.write(f"{lefich}\n")
      if testmp3 and not file_exists(lefich):
        print(f"\n\t>>>> inexistant : {lefich}")
    resultat.close()

def filtreligne(unechaine=None, ssrep=None):
  """
    Filtre une ligne de fichier m3u, alerte si contient un espace, ou plus d'un
    tiret et renvoie nom du fichier mp3

  [ EN ENTREE ]
      unechaine (chaine) une ligne du fichier m3u
      ssrep (chaine) un repertoire

  [ EN SORTIE ]
      unechaine (chaine)  nom du fichier mp3 retourné
                          suppression trailing-space.
                          alerte si contient un espace.
  """
  ### parametre local
  if ' ' in unechaine:
    print(f"\n\t>>>> au moins un espace : {ssrep} # {unechaine}")
  if unechaine.count('-') > 1:
    print(f"\n\t>>>> plus d'1 tiret : {ssrep} # {unechaine}")
  else:
    tamp = unechaine.split('-')
    if tamp[0].capitalize() != tamp[0]:
      print(f"\n\t>>>> majuscules : {ssrep} # {unechaine}")
  return unechaine.strip()

### Principal
if __name__ == "__main__":

  (CODE_RETOUR, SCOM, REP, TEST_PRESENCEFICMP3) = parametres(sys.argv)
  if CODE_RETOUR == 2:
    print(SCOM)
    action(REP, FICS_LISTE_TAMPON, FICS_LISTE, TEST_PRESENCEFICMP3)
  else:
    print(SCOM)
    sys.exit(1)
  sys.exit(0)
