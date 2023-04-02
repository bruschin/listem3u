#!/bin/bash
###########
## genere documentation avec sphinx
## nécessite d'avoir installé sphinx graphviz rhino
###########
export PATH=$PATH:~/opt/bin
REPTRAV="$(dirname $0)"
cd "docs" || exit 1

make -C ./ clean
#sphinx-build . _build
sphinx-apidoc -f -o ./ ../src
#sphinx-multiversion ./ _build/html
sphinx-build -b html ./ ./_build/html -D language=fr
#sphinx-build -b rinoh ./ ./_build/rinoh -D language=fr
sphinx-build -b epub ./ ./_build/html/epub/fr -D language=fr
exit 0

