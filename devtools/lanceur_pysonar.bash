#!/bin/bash
###########
## genere rapport remontee sonarqube
## nécessite d'avoir excute
## pip install pysonar
## https://docs.sonarsource.com/sonarqube-server/10.8/analyzing-source-code/scanners/sonarscanner-for-python/
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
FICSORTIE="${REPLOG}/pysonar-rapport.txt"
FICCONF="pyproject.toml"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}" 2>&1

echo "$0 : Lanceur pysonar"

pysonar --toml-path "${FICCONF}" --coverage-report-paths "public" || true

exec 1>&6 6>&-

cat "${FICSORTIE}"

echo "### $0 FIN ###"
exit 0
