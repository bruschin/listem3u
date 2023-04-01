#!/bin/bash
###########
## genere rapport pylint
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
#source /home/userdev/env/bin/activate
cd docs || exit 1
sphinx-build . _build
sphinx-apidoc -f -o ./ ../
sphinx-multiversion ./ _build/html
make clean html


