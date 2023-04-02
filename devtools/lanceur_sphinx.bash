#!/bin/bash
###########
## genere rapport pylint
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
export PATH=$PATH:~/opt/bin
REPTRAV="$(dirname $0)"
cd "docs" || exit 1

sphinx-build . _build
sphinx-apidoc -f -o ./ ../src
sphinx-multiversion ./ _build/html
make clean html
exit 0

