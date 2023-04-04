# listem3u [2023-04-02] 👉 BN V1.4 beta

![docs_pages_workflow](https://github.com/bruschin/listem3u/actions/workflows/
listem3u.yml/badge.svg)
[![Quality Gate Status](https://sonar.cloudmf.dev/api/project_badges/
measure?project=listem3u&metric=alert_status)](https://sonar.cloudmf.dev/dashboard?id=listem3u)

## Actions
+ configuration environnement github-pages ajout branche 3-sonarqube
  - Tentative configuration sonar

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
