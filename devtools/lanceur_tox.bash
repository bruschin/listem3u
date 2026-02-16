#!/bin/bash
###########
## genere rapport linter ruff
## nécessite d'avoir excute
## pip install ruff --user
## https://github.com/charliermarsh/ruff
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
REPCONF="docs"
FICSORTIE="${REPLOG}/tox-rapport.txt"
FICCONF="${REPCONF}/tox.ini"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ${PWD} ###"

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}" 2>&1

echo "$0 : Lanceur tox"

tox -c "${FICCONF}" --recreate

exec 1>&6 6>&-

cat "${FICSORTIE}"
echo "### $0 FIN ###"
exit 0
