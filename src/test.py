#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
    Created on 25 mars 2023

    @author: Nicolas Bruschi

    decryptage max_de_culture

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
        [2023-11-30] BN V1.0.0 :  Initialisation

    [REFERENCES]
        https://discord.com/channels/506449018885242890/1047540533616197662
"""

## Bibliotheques ##

import sys
import getopt
import os
import fnmatch
from datetime import datetime
from os.path import exists as file_exists

## Variables Globales ##

FILENAME = "test.py"
VERSION = f"\n {FILENAME} version : [2025-11-30 BN V1.0.0]"
FIC_TRAV = "/c/Users/matel/Downloads/test.txt"
USAGE = (f"\n  usage: {FILENAME} [OPTIONS]\n"
"  OPTIONS:\n"
"  [-h |--help : Demande usage] Optionnel\n"
"  [-f |--fichier]   <fichier de travail> OBLIGATOIRE.\n"
f"                      defaut si absent= {FIC_TRAV}\n"
"  [-v |--version : Demande version] Optionnel\n"
"  Tous les parametres acceptent casse minuscules/majuscules.\n")
NOW = datetime.now()
FICS_LISTE = f"test-{NOW.strftime('%d-%m-%Y')}.txt"

### Fonctions ###
#################

def parametres(argv):
    """
        Gestion des parametres d'appel = repertoire, help et version

       [ EN ENTREE ]
            argv = Les parametres d'appel du script

       [ EN SORTIE ]
            codeexit (entier) 0, 1 ou 2
            scom (chaine) commentaire
            fichier_travail (chaine)
    """
    ### parametre local
    codeexit = 0
    fichier_travail = FIC_TRAV  # valeur defaut
    oncontinue = 0  # si demande aide = 1 ou version = 10 ou les 2 = 11
    scom = ""  # commentaire si parametre imprevu
    nb_param = 0

    try:
        # pylint: disable=unused-variable
        options, remainder = getopt.getopt( argv[1:], "hHvVf:F:",
                                            ["help", "HELP",
                                            "version", "VERSION", "fichier=",
                                            "FICHIER=" ] )
        #print(f"debug param : {options},{remainder}\n")

        for opt, arg in options:
            nb_param += 1
            if opt.upper() in ["-H", "--HELP"]:
                oncontinue += 1
            elif opt.upper() in ("-F", "--FICHIER"):
                #print(f"debug {arg}")
                oncontinue = 0
                fichier_travail = arg
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
                    if not os.path.isfile(fichier_travail):
                        scom = f"\n\t>>>>FICHIER: {fichier_travail} "\
                                    "INACESSIBLE.\n"
                        codeexit = 1
                    else:
                        scom = "\n\t>>>>FICHIER CHOISI: "\
                            f"{fichier_travail} [OK]\n"
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

    return (codeexit, scom, fichier_travail)

def action(fic_tampon=None):
    """
        Gestion des parametres d'appel = repertoire, help et version

    [ EN ENTREE ]
        repert (chaine) repertoire de travail
        fic_tampon (chaine) fichier de travail
        fic (chaine) fichier resultat

    [ EN SORTIE ]
        constitution du fichier de sortie dans le repertoire de travail
        coderetour (entier) 0 OK - 1 KO
    """
    ### parametre local
    sunecom = ""
    decrypt = ""
    lignesresult = []

    try:
        if file_exists(FICS_LISTE):
            os.unlink(FICS_LISTE)
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        print(f"Something wrong with specified\
                    file {FICS_LISTE}. Exception- ", sys.exc_info())
        return 1
    
    with open(fic_tampon,"r", encoding="utf-8") as lefic:
        for ligne in lefic:
            if _estexploitable(ligne):
                # filtre sur ligne contenant des blancs...
                decrypt = _decrypteligne(ligne)
                lignesresult.append(decrypt)
    lefic.close()
    with open(FICS_LISTE,"a",encoding="utf-8") as resultat:
        for elmt in lignesresult:
            resultat.write(f"\n{elmt}")
    resultat.close()
    return 0, sunecom

### Sous Fonctions ###
######################

def _find(pattern, path):
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
    #print(f"debug _find {result}")
    return result

def _estexploitable(unechaine=None):
    """
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
            

def _decrypteligne(unechaine=None):
    """
        Filtre une ligne de fichier m3u, alerte si contient un espace, ou plus
        d'un tiret et renvoie nom du fichier mp3

    [ EN ENTREE ]
        unechaine (chaine) une ligne du fichier m3u
        ssrep (chaine) un repertoire

    [ EN SORTIE ]
        unechaine (chaine)  nom du fichier mp3 retourné
                            suppression trailing-space.
                            alerte si contient un espace.
    """
    ### parametre local
    chainecrypt   = "abcdefghijklmnopqrstuvwxyz0123456789',.!?"
    chainedecrypt = "defghijklmnopqrstuvwxyzabc0123456789',.!?"
    
    
    resultat=""
    longueur = len(unechaine)
    for i in range(0,longueur):
        if unechaine[i] == ' ':
            resultat += " "
        else:
            k = 0
            for k in range(0,41):
                maj = False
                if unechaine[i] != unechaine[i].lower():
                    maj = True
                if chainecrypt[k] == unechaine[i].lower():
                    if maj:
                        resultat += chainedecrypt[k].upper()
                    else:
                        resultat += chainedecrypt[k]                        
                    break 

    return resultat

### Principal ####
##################

# pragma: no cover
if __name__ == "__main__":
    (CODERETOUR, SCOM, FIC) = parametres(sys.argv)
    if CODERETOUR == 2:
        print(SCOM)
        (CODERETOUR,SCOM) = action( FIC )
    print(SCOM)
    sys.exit(CODERETOUR)
