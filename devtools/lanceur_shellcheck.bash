#!/bin/bash
###########
## genere rapport doxygen
## nécessite d'avoir installé doxygen dia et généré le fichier Doxyfile
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
FICSORTIE="${REPLOG}/shellcheck-rapport.txt"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}" 2>&1

echo "$0 : shellchek divers scripts bash"

shellcheck -f json src/listem3u.bash src/prepare_tests.bash

exec 1>&6 6>&-

cat "${FICSORTIE}"
#rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
echo "### $0 FIN ###"
exit 0
