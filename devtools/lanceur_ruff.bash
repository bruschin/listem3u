#!/bin/bash
###########
## genere rapport linter ruff
## nécessite d'avoir excute
## pip install ruff --user
## https://github.com/charliermarsh/ruff
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
FICSORTIE="${REPLOG}/ruff-rapport.txt"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}"

ruff check --fix src
ruff format src

exec 1>&6 6>&-

cat "${FICSORTIE}"
#rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
echo "### $0 FIN ###"
exit 0

