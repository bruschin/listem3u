#!/bin/bash
###########
## genere rapport pytest
###########
REPTRAV="$(dirname "$0")"
VERSION_PYTHON="$1"
if test -z "${VERSION_PYTHON}"; then
  # gestion valeur defaut
  VERSION_PYTHON="3.12"
fi

REPLOG="rapports"
REPCONF="docs"
REPTESTS="${REPLOG}/htmlcov/${VERSION_PYTHON}"
FICSORTIE="${REPLOG}/pytest-rapport.${VERSION_PYTHON}.txt"
FICCONF="${REPCONF}/pytest.ini"
export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPTESTS}"; then
  mkdir -p "${REPTESTS}" 2>/dev/null
fi

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}"

pytest  -c "${FICCONF}" -q "src/"
pytest  -c "${FICCONF}" \
	--cov-config="${REPCONF}/.coveragerc" \
	--cov-report xml:"${REPLOG}/coverage.${VERSION_PYTHON}.xml" \
	--cov-report=html:"${REPTESTS}" \
	--cov="src/"

exec 1>&6 6>&-

cat "${FICSORTIE}"
#rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null

echo "### $0 FIN ###"
exit 0
