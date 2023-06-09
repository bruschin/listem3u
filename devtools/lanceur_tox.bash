#!/bin/bash
###########
## genere rapport linter ruff
## nécessite d'avoir excute
## pip install ruff --user
## https://github.com/charliermarsh/ruff
###########
REPTRAV="$(dirname $0)"
FICSORTIE="rapports/tox-rapport.txt"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

exec 6>&1
exec >"${FICSORTIE}"

tox -c devtools/tox.ini --recreate > "${FICSORTIE}" 2>/dev/null

exec 1>&6 6>&-

cat "${FICSORTIE}"
rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
if test -f "rapports/coverage2.xml"; then
    cat "rapports/coverage2.xml"
fi
echo "### $0 FIN ###"
exit 0
