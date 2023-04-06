#!/bin/bash
###########
## genere rapport pytest
###########
FICSORTIE="pytest-report.txt"
REPTRAV="$(dirname $0)"
export TZ="Europe/Paris"

echo "### $0 DEBUT ###"

exec 6>&1
exec >"${FICSORTIE}"


cd "${REPTRAV}/.." || exit 1

pytest  --report-log=src/reports/ -c devtools/pytest.ini -q src/
pytest  --report-log=src/reports/ -c devtools/pytest.ini --cov=listem3u \
				--cov-report=xml --cov-report=html -q src/

exec 1>&6 6>&-

cat "${FICSORTIE}"
rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null

echo "### $0 FIN ###"
exit 0

