#!/bin/bash
###########
## genere rapport doxygen
## nécessite d'avoir installé doxygen dia et généré le fichier Doxyfile
###########
REPTRAV="$(dirname "$0")"
FICSORTIE="src/shellcheck-rapport.json"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

exec 6>&1
exec >"${FICSORTIE}"

shellcheck -f json src/listem3u.bash > "${FICSORTIE}"

exec 1>&6 6>&-

cat "${FICSORTIE}"
#rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
echo "### $0 FIN ###"
exit 0

