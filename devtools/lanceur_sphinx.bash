#!/bin/bash
###########
## genere documentation avec sphinx
## nécessite d'avoir installé sphinx graphviz rhino
## gestion version dans conf.py gérée par mef_versions.bash
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
FICSORTIE="${REPLOG}/sphinx-rapport.txt"
REPCONF="docs"
FICCONFGITLAB="${REPCONF}/conf_gitlab.py"
FICCONFGITHUB="${REPCONF}/conf_github.py"
FICCONF="${REPCONF}/conf.py"
VERSION_PYTHON="$1"


export GIT_PYTHON_REFRESH=quiet
export GIT_PYTHON_GIT_EXECUTABLE="/usr/bin/git"
export TZ="Europe/Paris"
export REPO_NAME

cd "${REPTRAV}/.." || exit 1
echo -e "### $0 DEBUT ###\n"

if [[ -z "${VERSION_PYTHON}" ]] ; then
  # gestion valeur defaut
  REPO_NAME='https://bruschin.github.io/listem3u'
  if [[ -f "${FICCONFGITHUB}" ]]; then
    \cp -f "${FICCONFGITHUB}" "${FICCONF}" 1>/dev/null 2>/dev/null
  fi
else
  REPO_NAME='https://listem3u-d8b643.gitlab.meteo.fr/'
  if [[ -f "${FICCONFGITLAB}" ]]; then
    \cp -f "${FICCONFGITLAB}" "${FICCONF}" 1>/dev/null 2>/dev/null
  fi
fi

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}" 2>&1

echo "$0 : Génération documentation par sphinx des scripts python sous src"

#précautions répertoires sous build
reps_utils="build/sphinx-html build/sphinx-epub"
for direct in ${reps_utils}; do
  if ! test -d "${direct}"; then
    mkdir -p "${direct}" 2>/dev/null || true
  fi
done

(
        echo "### INFO: cleaning ###"
        make -C docs clean
        echo "### INFO: Building html for french language ###"

        sphinx-build -a -v -c docs -b html docs build/sphinx-html
        #echo "### INFO: Building epub for french language ###"
        #sphinx-build -a -v -c docs -b epub docs build/sphinx-epub
)

exec 1>&6 6>&-

cat "${FICSORTIE}"
echo -e "\n### $0 FIN ###"
exit 0
