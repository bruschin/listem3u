#!/bin/bash
###########
## genere rapport linter ruff
## nécessite d'avoir excute
## pip install ruff --user
## https://github.com/charliermarsh/ruff
###########
export TZ="Europe/Paris"
REPTRAV="$(dirname $0)"
cd "${REPTRAV}/.." || exit 1

FICSORTIE="ruff-report.txt"
ruff src/*py > "${FICSORTIE}"
cat "${FICSORTIE}"
rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
exit 0

