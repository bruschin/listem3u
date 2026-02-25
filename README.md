# Projet listem3u [2026-02-23] 👉 BN V2.0.1

[![GITHUB Actions status](https://github.com/bruschin/listem3u/actions/workflows/listem3u_steps.yml/badge.svg?branch=releases))](https://github.com/bruschin/listem3u/actions/workflows/listem3u_steps.yml) [![SonarQube Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bruschin_listem3u&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=bruschin_listem3u)
<!--[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0b206f1af71d47dcb8092d1d9069aebb)](https://app.codacy.com/gh/bruschin/listem3u/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)-->
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/summary/new_code?id=bruschin_listem3u)
<!-- [![Quality Gate Status](https://sonar.cloudmf.dev/api/project_badges/measure?project=listem3u&metric=alert_status)](https://sonar.cloudmf.dev/dashboard?id=listem3u)-->

## Projet listem3u

> Ce programme python d'exercice, ludique et pratique, fait partie d'un projet d'étude plus vaste nommé = **Hareng Rouge**. Il exploite des fichiers de type Playlist audio, d'extension .m3u, contenus dans les sous-répertoires, d'un repertoire de travail, passé en paramètre d'appel. Au final, il est censé produire un fichier de playlist intégrale de fichiers audio mp3, classés par sous-dossier et ordre alphabétique, permettant de les lire de façon continue ou aléatoire, une fois raccordé, par exemple, à l'autoradio d'une voiture, via une clé USB.
Testé OK sur Fiat 500 et Peugeot 3008.

## Spécifications évolutives au fil du temps

### Règles de nommage

- L'arborescence des sous-répertoires du répertoire de travail

> Elle doit respecter un nommage numérique formatté du type %03d et incrémental : **001,002,...,013,...,0XY,etc.**
Aucun contrôle n'est implémenté pour s'assurer du respect de cette règle !
Chaque sous-répertoire de nom = 0XY, contient **au plus 100** fichiers audio mp3, de nom = (sans espace, ni accent) et un fichier 0XY-Playlist.m3u unique, chargé de les référencer tous.
Le répertoire **automation**, prévu pour faire reposer les test unitaires sur des exemples concrêts, expose de façon plus explicite, ces règles.
Lors du traitement, des alertes sur le nommage des fichiers peuvent remonter. Ajoutés, pour signaler la présence d'espaces oubliés, de majuscules trop nombreuses, etc.

- Un fichier audio est généralement nommé :

> Exemple : Ca_va_peter-Chouf.mp3
Première lettre du titre du morceau en majuscule
Les espaces sont remplacés par un "_"
Un tiret "-" sert à séparer titre et nom de l'interprète, groupe, musicien. Parfois un "&" pour séparer plusieurs artistes.

### Exemples d'alertes

- listem3u.py -m -r /d/Morceaux_choisis
- plus d'1 tiret : 009 # La_wally_ebben_ne_andro_lontana-Maria_Callas-Alfredo_Catalani.mp3
  - Il faudrait utiliser "**&**" : La_wally_ebben_ne_andro_lontana-Maria_Callas&Alfredo_Catalani.mp3
- majuscules : 008 # Peeping_Tom-Jamie_Berry&Rosie_Harte.mp3
  - Il faudrait renommer en : Peeping_tom-Jamie_Berry&Rosie_Harte.mp3
- une alerte signale la présence d'un espace dans une référence de la Playlist
- avec l'argument -m si le fichier mp3 référencé dans le fichier 0XY-Playlist.m3u n'est pas disponible dans le répertoire 0XY une alerte doit le signaler.

## Paramètres

```python
[-h |--help : Demande usage] # Optionnel

[-m |--mp3 : Verification existence fic mp3] # Optionnel. Defaut = False
[-r |--repertoire] <repertoire de travail> # Optionnel. Defaut = ${Repertoire_travail}
[-v |--version : Demande version] # Optionnel.
# Tous les parametres acceptent casse minuscules/majuscules
```

## Sortie

```python
0 OK # Constitution dans le repertoire de travail du fichier de sortie
1 KO # Affichage de la raison de l'échec
```

## Forge logiciel

- Listem3u est produit avec Visual Studio Code, sur Linux ubuntu 24.04 et sur Windows 11. Extensions et configuration utilisées de cette IDE prévues pour être documentées. Listem3u sur Github, utilise les Github-Actions via un pipeline Ci/CD, pour construire dans un docker, les environnements virtuels python3 nécessaires, pour "Linter" le code (Pylint, Shellcheck, ruff), exécuter les tests unitaires prévus sans erreur ni régression, soumettre le code python à sonarqube.io et s'assurer de franchir une barrière de qualité, auto-documenter le code avec sphinx et doxygen, et alimenter une page web hébergé sur Github Pages, avec les logs de ces actions, la documentation produite, des liens construits. Ce projet est également installé sur une instance Gitlab d'entreprise, avec un serveur de dockers interne, des gitlab-runners internes, et via gitlab CI/CD, Gitlab Pages, Wiki, il produit des choses similaires, un package wheel qui intégre automatiquement, un dépôt Pypi Nexus réservé. Snapshot ou release.

## [Changelog]

## Memo configuration environnement mini-conda

- Conda config --add channels conda-forge

- conda create -n myenv python=3.10
  - conda activate myenv
  - conda install pylint
  - conda install pytest
  - conda install ruff
  - conda install sphinx
  - conda install sphinx_rtd_theme
  - conda install sphinxcontrib-serializinghtml
  - conda install graphviz

- Pour extraire l'environnement conda et l'importer
  - conda list -e > requirements_conda.txt
  - conda create --name "environment_name" --file requirements_conda.txt
  - conda install --file requirements_conda.txt

## Documentations

- [reStructuredText](https://docutils.sourceforge.io/rst.html)
- [documentation des modules python du projet](https://bruschin.github.io/listem3u/)
- [wiki du projet](https://bruschin.github.io/listem3u/wiki)

[Changelog]: Changelog.md
