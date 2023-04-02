#!/bin/bash
###########
## genere documentation avec sphinx
## nécessite d'avoir installé sphinx graphviz rhino
###########
export TZ="Europe/Paris"
REPTRAV="$(dirname $0)"
cd "docs" || exit 1

make -C ./ clean
#sphinx-build . _build
sphinx-apidoc -f -o ./ ../src
#sphinx-multiversion ./ _build/html
languages="en $(find ./locales/ -mindepth 1 -maxdepth 1 -type d \
                -exec basename '{}' \;)"

# make the current version = main available to conf.py
#current_version="main"
export current_version="main"

echo "INFO: Building sites for ${current_version}"

for current_language in ${languages}; do

  # make the current language available to conf.py
  export current_language

  ##########
  # BUILDS #
  ##########
  echo "INFO: Building for ${current_language}"

  # HTML #
  sphinx-build  -b "html" "./" "./_build/html" \
                -D language="${current_language}"

  # EPUB #
  sphinx-build  -b "epub" "./" "./_build/html/epub" \
                -D language="${current_language}"

  # PDF #
  #sphinx-build -b rinoh ./ ./_build/html/rinoh/fr -D language=fr
done

exit 0

