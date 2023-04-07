#!/bin/bash
###########
## genere rapport pylint
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
REPTRAV="$(dirname $0)"
FICSORTIE="rapports/pylint-rapport.txt"
export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

exec 6>&1
exec >"${FICSORTIE}"

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

exec 1>&6 6>&-

cat "${FICSORTIE}"
rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
echo "### $0 FIN ###"
exit 0

