#!/bin/bash
###########
## genere rapport doxygen
## nécessite d'avoir installé doxygen dia graphviz et généré le fichier Doxyfile
## gestion version dans Doxyfile gérée par mef_versions.bash
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
REPCONF="docs"
REPDOXYGEN="${REPLOG}/doxygen"
FICSORTIE="${REPLOG}/doxygen-rapport.txt"
FICCONF="${REPCONF}/Doxyfile"
export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPDOXYGEN}"; then
  mkdir -p "${REPDOXYGEN}" 2>/dev/null
fi

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}" 2>&1

echo "$0 : Génération documentation par Doxygen"
doxygen "${FICCONF}"

exec 1>&6 6>&-

cat "${FICSORTIE}"
echo "### $0 FIN ###"
exit 0

