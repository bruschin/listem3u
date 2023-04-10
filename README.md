# listem3u [2023-04-09] 👉 BN V1.6

![docs_pages_workflow](https://github.com/bruschin/listem3u/actions/workflows/listem3u.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=bruschin_listem3u&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=bruschin_listem3u&branch=5-v15b)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0b206f1af71d47dcb8092d1d9069aebb)](https://app.codacy.com/gh/bruschin/listem3u/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
<!--[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/summary/new_code?id=bruschin_listem3u)
 [![Quality Gate Status](https://sonar.cloudmf.dev/api/project_badges/measure?project=listem3u&metric=alert_status)](https://sonar.cloudmf.dev/dashboard?id=listem3u)-->

## Action V1.6

+ tester executeur local pour github action
+ regarder doxygen + shellcheck
+ branch main n'accepte plus les pushs sans merger cf règles définies.

## Actions V1.5

+ Couverture de code dans sonar
+ Pipeline yaml en plusieurs steps
+ Une issue -> une branche et une pull request pour merger ok

## Actions V1.4

+ Configuration environnement github-pages ajout branche 3-sonarqube
+ Tentative configuration sonar

## Configuration environnement mini-conda

+ conda config --add channels conda-forge

+ conda create -n myenv python=3.10
  + conda activate myenv
  + conda install pylint
  + conda install pytest
  + conda install ruff
  + conda install sphinx
  + conda install sphinx_rtd_theme
  + conda install sphinxcontrib-serializinghtml
  + conda install graphviz

+ Pour extraire l'environnement conda et l'importer
  + conda list -e > requirements_conda.txt
  + conda create --name <environment_name> --file requirements_conda.txt
  + conda install --file requirements_conda.txt

## Documentations

+ [reStructuredText](https://docutils.sourceforge.io/rst.html)
+ [documentation des modules pyhton du projet](https://bruschin.github.io/listem3u/)
+ [wiki du projet](https://bruschin.github.io/listem3u/wiki)
