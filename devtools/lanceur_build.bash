#!/bin/bash
###########
## genere package wheel listem3u
## pip install builf --user
## https://packaging.python.org/en/latest/tutorials/packaging-projects/
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
REPBUILD="dist"
FICSORTIE="${REPLOG}/build-rapport.txt"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPBUILD}"; then
  mkdir -p "${REPBUILD}" 2>/dev/null
fi

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}" 2>&1

echo "$0 : Lanceur packaging build"

python3 -m build

exec 1>&6 6>&-

cat "${FICSORTIE}"

echo "### $0 FIN ###"
exit 0
