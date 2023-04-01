#!/bin/bash
###########
## genere rapport pytest
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
#source /home/userdev/env/bin/activate
#REPTRAV="$(dirname $0)"
#cd "${REPTRAV}/.." || exit 1

FICSORTIE="pytest-report.txt"
pytest -q src/test_listem3u.py  \
    > "${FICSORTIE}"
cat "${FICSORTIE}"
rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
exit 0

