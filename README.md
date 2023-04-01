# listem3u [2023-04-01] 👉 BN V1.3

![docs_pages_workflow](https://github.com/bruschin/listem3u/actions/workflows/
listem3u.yml/badge.svg)

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
