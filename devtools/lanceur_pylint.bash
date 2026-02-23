#!/bin/bash
###########
## genere rapport pylint
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
# https://pypi.org/project/isort/
# https://pypi.org/project/black/
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
REPCONF="docs"
FICCONF="${REPCONF}/.pylintrc"
FICSORTIE="${REPLOG}/pylint-rapport.txt"
export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}"

echo "$0 : Linter des fichiers python sous src"

sed -i -e "s@indent-string='    '@indent-string='  '@g" "${FICCONF}"
pylint \
    --rcfile \
    "${FICCONF}" \
    src/listem3u.py \
    tests/test_listem3u.py \
    src/test.py \
    -r \
    n \
    --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
    -d E0015 \
    -d C0325 \
    -d C0303 \
    -d W0603 \
    -d W0703 \
    -d W0105 \
    -d W0311 \
    -d R0801 \
    -d too-many-arguments \
    -d too-many-branches 

exec 1>&6 6>&-

cat "${FICSORTIE}"
#rm -f "${FICSORTIE}" 1>/dev/null 2>/dev/null
echo "### $0 FIN ###"
exit 0

