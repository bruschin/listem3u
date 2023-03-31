#!/bin/bash
###########
## genere rapport pytest
## nécessite d'avoir excute
## pylint --generate-rcfile > .pylintrc
###########
#source /home/userdev/env/bin/activate
pytest -q ./test_listem3u.py  \
    > pytest-report.txt
cat pytest-report.txt

