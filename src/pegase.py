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

  [ EN ENTREE ]
    1 ou 3 arguments de type chaine = xxhmm ou xHmm
        exemple 9h24 ou 09:24 ou 13H56 (:,h central accepte la casse min/maj)
        Si un seul arg on appliquera automatiquement une pause midi obligatoire
        de 45 minutes
        Si 3 arg la duree entre arg 2 et arg 3 est la duree de la pause
        meridienne ne pouvant etre inf a 45 minutes.
  [ EN SORTIE ]
    0   OK => Affichage de l'heure du depart calcule ex: DEPART : 17H19
    1   KO Arguments appel incorrects ou en nombre incorrect.
        => Affichage raison pb.

  [VERSIONS]
    [2023-03-14] BN V1.0 : Initialisation
"""

## Bibliotheques ##

import sys
import getopt

# VARIABLES GLOBALES :

FILENAME = "pegase.py"
VERSION = f"  {FILENAME}: [2023-03-14] BN V1.0\n"
USAGE = (f"  usage: {FILENAME} [OPTIONS]\n" +\
"  OPTIONS:\n"
"  [09:31 - 12h00 - 12H38] 1 ou 3 badgeage(s) OBLIGATOIRE(S)\n" +\
"  [-h |--help : Demande usage] Optionnel\n" +\
"  [-v |--version : Demande version] Optionnel\n"
"  Tous les parametres acceptent casse minuscules/majuscules.\n")
DUREE_JOUR = 444  # 7h24 convertis en minutes (37h sur 5 j = 7h24 par jour)
DUREE_PAUSE_DEFAUT = 45
SEPARHM = ["H",":"]

## Fonctions :
##############

def parametres(argv):
  """_
    Gestion des parametres d'appel = help et version

  [ EN ENTREE ]
      argv = Les parametres d'appel du script

  [ EN SORTIE ]
      0   OK => Affichage : aide usage ou version
      1   KO => arguments appel incorrects ou en nombre incorrect.
             => Affichage raison Pb
      Rien   => parametres ne contiennent pas de demande d'aide ou de version on
                sort et continue
  """
  try:

    # pylint: disable=unused-variable
    args,opts = getopt.getopt( argv[1:], "hHvV", ["help","HELP",
                                                   "version", "VERSION"])
  except getopt.GetoptError as err:
    print( f'\n\t>>>> ERREUR: {str(err)}\n')
    print( f"{USAGE}" )
    sys.exit(1)

  # pylint: disable=unused-variable
  for opt in opts:
    if opt in ["-h", "-H", "--help", "--HELP"]:
      print( f"{USAGE}" )
      sys.exit(0)
    elif opt in ("-v", "-V", "--version", "--VERSION"):
      print( f"{VERSION}" )
      sys.exit(0)

def gestion_parametre(*args):
  """

    Gestion des parametres d'appel

    [ EN ENTREE ]
      *args = Tous les parametres d'appel du script

    [ EN SORTIE ]
      minutesici (tableau d'entier) des minutes calculées.

      ou bien sortie code

      1   KO arguments appel incorrects ou en nombre incorrect.
          => Affichage raison Pb

  """
  # Variables locales:
  ####################
  minutesici = []
  if len(args[0]) == 0:
    print( '\n\t>>>> ERREUR: Au moins un badgeage OBLIGATOIRE\n')
    print( f"{USAGE}" )
    sys.exit(1)

  for chaine in args[0]:
    #print('debug 1',args[0],chaine)
    # controle au moins un param non vide
    # on passe la chaine en majuscule et on supprime tous les espaces
    ch_trav = chaine.upper().replace(" ","")
    longueur = len(ch_trav)
    #print ('debug 2', ch_trav, longueur, chaine)

    if longueur == 0:
      print( "\n\tNombre de badgeage insuffisant\n")
      print( f"{USAGE}" )
      sys.exit(1)
    elif 4 <= longueur <= 5:
      # la liste non vide est-elle un badgeage ?
      minutesici = test_est_un_badgeage_valide( ch_trav, minutesici)
      #print(f'debug 6 {minutesici}')
    elif longueur != 1:
      # la liste non vide n'est pas un separateur conforme
      #print(f'debug 5 {ch_trav}')
      print( f"\nSeparateur badgeages = {ch_trav} non conforme\n")
      sys.exit(1)
    #else:
      # la liste non vide est un separateur conforme
  return minutesici

def test_est_un_badgeage_valide(ch_trav, conversion):
  """
    la liste non vide traitée est-elle un badgeage ?

  [ EN ENTREE ]
      ch_trav (chaine) badgeage ?
      conversion (tableau d'entier) badgeage hh:mm converti en minute

    [ EN SORTIE ]
      conversion (tableau d'entier) avec ce badgeage en plus

      ou bien sortie code

      1   KO si pas un badgeage valide on sort
          => Affichage raison Pb
  """
  # la chaine de la liste de bonne longueur est-elle un badgeage ?
  # separateur entre h et minute
  separateur = ""
  # pylint: disable=unused-variable
  for count,sep in enumerate(SEPARHM):
    if sep in ch_trav:
      separateur = sep
  if separateur == "":
    print( f"\n\tBadgeage = {ch_trav} non conforme\n")
    print( f"{USAGE}" )
    sys.exit(1)
  else:
    sheure,sminute = ch_trav.split(separateur)
    try:
      sheure = int(sheure, base=10)
      sminute = int(sminute, base=10)
      conversion.append(conversion_minutes(sheure,sminute))
    except ValueError:
      print( f"\n\tBadgeage = {ch_trav} non conforme\n")
      sys.exit(1)
    #print(f'debug 4 {sheure} {sminute}')
    return conversion

def conversion_minutes(desheures,desminutes):
  """_
    Conversion heures et minutes passe en appel (de type hh et mm)
    en un entier = minutes

    [ EN ENTREE ]
      desheures (entier) 09 converti en 9
      desminutes (entier)

    [ EN SORTIE ]
      minutes : entier exemple 9*60 + 15 = 555

  """
  # Variables locales
  int_conv_retour=0

  int_conv_retour = (60 * desheures) + desminutes
  return int_conv_retour

def conversion_heures(desminutes):
  """_
    Conversion des minutes en xHmm

    [ EN ENTREE ]
      desminutes (entier)

    [ EN SORTIE ]
      ch_conv_retour (chaine) formatee
  """
  # Variables locales
  ch_conv_retour=""
  lesheures = 0
  lesminutes = 0

  lesheures = desminutes // 60
  lesminutes = desminutes % 60
  ch_conv_retour = f"{lesheures}H{lesminutes}"
  return ch_conv_retour

def traitement(tabminutes):
  """
    affichage finale selon nombre de badgeages recupérés.

    [ EN ENTREE ]
      tabminutes (tableau d'entier)

    [ EN SORTIE ]
      ch_conv_retour (chaine) formatee
  """
  uncompteur = len(tabminutes)
  match uncompteur:
    case 3:
      pause = max((tabminutes[2] - tabminutes[1]), DUREE_PAUSE_DEFAUT)
      soir = tabminutes[0] + pause + DUREE_JOUR
      depart = conversion_heures(soir)
      print( f"depart : {depart}")
    case 1:
      soir = tabminutes[0] + DUREE_PAUSE_DEFAUT + DUREE_JOUR
      depart = conversion_heures(soir)
      print( f"depart : {depart}")
    case _:
      print( f'\n\t>>>> ERREUR: Nombre badgeage {uncompteur} imprevu\n')
      sys.exit(1)

### Principal
if __name__ == "__main__":
  parametres(sys.argv)
  minutes = gestion_parametre(sys.argv[1:])
  traitement(minutes)
  sys.exit(0)
