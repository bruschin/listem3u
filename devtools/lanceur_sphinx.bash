#!/bin/bash
###########
## genere documentation avec sphinx
## nécessite d'avoir installé sphinx graphviz rhino
###########
export TZ="Europe/Paris"
export REPO_NAME='https://bruschin.github.io/listem3u'

REPTRAV="$(dirname "$0")"
cd "${REPTRAV}/../docs" || exit 1

make -C ./ clean
#sphinx-build . _build
sphinx-apidoc -f -o ./ ../src
#sphinx-multiversion ./ _build/html

### generation entree index.html pour https://bruschin.github.io/listem3u
#sphinx-build  -b "html" "./" "./_build/html"

langues="$(find ./locales/ -mindepth 1 -maxdepth 1 -type d \
                -exec basename '{}' \;)"

# make the current version = main available to conf.py
#current_version="main"
export current_version="main"

echo "INFO: Building sites for ${current_version}"

for current_language in ${langues}; do

  # make the current language available to conf.py
  export current_language

  ##########
  # BUILDS #
  ##########
  echo "### INFO: Building for ${current_language} ###"

  # HTML #
  if test "${current_language}" == "fr"; then
    sphinx-build  -b "html" "./" "./_build/html" -D language="fr"
  fi

  # EPUB #
  sphinx-build  -b "epub" "./" "_build/html/epub" \
                -D language="${current_language}"

  # PDF #
  #sphinx-build -b rinoh ./ ./_build/html/rinoh/fr -D language=fr
done

exit 0

