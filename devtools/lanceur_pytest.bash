#!/bin/bash
###########
## genere rapport pytest
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
export TZ="Europe/Paris"
REPTRAV="$(dirname $0)"
cd "${REPTRAV}/.." || exit 1

FICSORTIE="pytest-report.txt"
#pytest -q src/test_listem3u.py > "${FICSORTIE}"
pytest  -c devtools/pytest.ini -q src > "${FICSORTIE}"
pytest  -c devtools/pytest.ini -q src/ -W error::UserWarning \
        --cov --cov-report=xml --cov-report=html
cat "${FICSORTIE}"
rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
exit 0

