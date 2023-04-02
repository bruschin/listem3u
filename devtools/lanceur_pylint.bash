#!/bin/bash
###########
## genere rapport pylint
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
REPTRAV="$(dirname $0)"
cd "${REPTRAV}/.." || exit 1

FICSORTIE="pylint-report.txt"
sed -i -e "s@indent-string='    '@indent-string='  '@g" src/.pylintrc
pylint \
    --rcfile \
    src/.pylintrc \
    src/listem3u.py \
    src/test_listem3u.py \
    src/pegase.py \
    -r \
    n \
    --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
    -d C0325 \
    -d W0603 \
    -d W0703 \
    -d W0311 \
    -d R0801 \
    -d too-many-arguments \
    -d too-many-branches \
    > "${FICSORTIE}"
cat "${FICSORTIE}"
rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
exit 0

