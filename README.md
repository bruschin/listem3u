# Projet listem3u [2026-03-03] 👉 BN V2.0.2

[![GITHUB Actions status](https://github.com/bruschin/listem3u/actions/workflows/listem3u_steps.yml/badge.svg?branch=releases))](https://github.com/bruschin/listem3u/actions/workflows/listem3u_steps.yml) [![SonarQube Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bruschin_listem3u&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=bruschin_listem3u)
<!--[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0b206f1af71d47dcb8092d1d9069aebb)](https://app.codacy.com/gh/bruschin/listem3u/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)-->
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/summary/new_code?id=bruschin_listem3u)
<!-- [![Quality Gate Status](https://sonar.cloudmf.dev/api/project_badges/measure?project=listem3u&metric=alert_status)](https://sonar.cloudmf.dev/dashboard?id=listem3u)-->

## ![Projet listem3u.png](docs/listem3u.png "Projet listem3u"){ width="64" height="64" style="display: inline; margin: 0 auto; vertical-align: middle;" } Projet listem3u

> Ce programme python d'auto-apprentissage pratique, pédagogique et ludique, fait partie d'une ambition d'étude plus vaste, baptisée = **Hareng Rouge**. Il exploite des fichiers de type Playliste audio, d'extension ".m3u", contenus dans les sous-répertoires, d'un repertoire de travail, lui même, renseigné en paramètre d'appel. Au final, il est censé produire un fichier daté, **"000-liste-AA-MM-YYYY.m3u"**, Playliste intégrale de fichiers audio mp3, référencés par sous-dossier et ordre alphabétique. Cette playliste permet de les lire, de façon continue ou aléatoire, une fois raccordé, par exemple, à l'autoradio d'une voiture, via une clé USB.
Testé compatible Fiat 500 et Peugeot 3008.

## Spécifications règles et convenances

Evolutives depuis les débuts du développement.

Le répertoire **automation**, prévu pour faire reposer les test unitaires sur des exemples concrets, expose de façon plus explicite, ce qui suit.

- ### Sous-répertoires, du répertoire de travail

  #### Nommage numérique formatté de type %03d et incrémental : 001,002,...,013,...,0XY

    > Attention ! Aucun contrôle n'est implémenté pour s'assurer du respect de cette règle ! L'algorithme de traitement en dépend.

  #### Au plus 100 fichiers audio par sous-répertoire 0XY
  
    > Moyen mnémotechnique pratique pour situer un morceau en cours d'écoute.
    Si affiché sur l'autoradio : 256eme fichiers sur 1206 => Le répertoire de stockage du morceau est le 003. **Du 1er au 100e => 001. Du 1101e au 1200e => 012**
    Permet également de comparer facilement le nombre de fichiers audio stockés au nombre de ceux référencés dans la Playliste totale produite.

  #### Un fichier Playliste unique par sous-répertoire 0XY

    > Nommé 0XY-Playlist.m3u.
    Il référencie les fichiers audio du répertoire 0XY, classés par ordre alphabétique de nom.
    Premiere ligne : #EXTM3U
    Deuxième ligne : #PLAYLIST:0XY
    Pas de dernière ligne vide
    Au max 102 lignes par Playliste de sous-répertoire.

- ### Fichiers audio

  #### Nommés sans accent, ni espace
  
  > **Espaces** remplacés par **"_"**

  #### Première lettre du titre du morceau en Majuscule

  #### Un tiret "-" sépare le titre du nom de l'interprète, groupe ou musicien

  #### Une esperluette "&" sépare plusieurs artistes
  
  > Exemples :
  Ca_va_peter-Chouf.mp3
  I_want_a_new_drug-Huey_Lewis_&_The_News.mp3

- ### Répertoire de travail

  > L'étude des fichiers 00n-Playlist.m3u contenus dans les sous-répertoires 00n
  du répertoire de travail passé en argument d'appel ou par omission fixé en dur
  dans le code, permet d'y produire un fichier temporaire de nom
  000-liste-JJ-MM-AAAA.prod qui sera comparé sha512sum au précédent fichier
  000-liste-JJ-MM-AAAA.m3u si existant. En cas d'égalité de signature le fichier
  m3u existant est laissé en l'état, pas de différence de production. En cas
  d'inégalité le fichier 000-liste-JJ-MM-AAAA.prod est renommé
  000-liste-JJ-MM-AAAA.m3u en remplacement, écrasement du précédent.

## Traitement

Des **alertes** sur les règles de nommage des fichiers peuvent remonter.
Elles furent ajoutées, pour signaler la présence d'espaces oubliés, de majuscules trop nombreuses, etc. mais ne sont pas bloquantes.

### Exemples d'alertes

  ```python
  listem3u.py -m -r /d/Morceaux_choisis
  ```

- Plus d'1 tiret : 009 # La_wally_ebben_ne_andro_lontana-Maria_Callas-Alfredo_Catalani.mp3
  > Il vaudrait mieux utiliser "**&**" : exemple :
  **La_wally_ebben_ne_andro_lontana-Maria_Callas&Alfredo_Catalani.mp3**
- majuscules : 008 # Peeping_Tom-Jamie_Berry&Rosie_Harte.mp3
  > Il vaudrait mieux renommer en : **Peeping_tom-Jamie_Berry&Rosie_Harte.mp3**
- Une alerte signale la présence d'un espace dans une référence de la Playliste
- > Avec l'argument d'appel optionnel **-m** si le fichier mp3 référencé dans le fichier 0XY-Playlist.m3u n'est pas disponible dans le répertoire 0XY une alerte le signale.

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
