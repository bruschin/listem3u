#!/bin/bash
###########
## genere rapport pylint
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
#source /home/userdev/env/bin/activate
sed -i -e "s@indent-string='    '@indent-string='  '@g" .pylintrc
pylint \
    --rcfile \
    .pylintrc \
    listem3u.py \
    test_listem3u.py \
    pegase.py \
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
    > pylint-report.txt
cat pylint-report.txt

