#!/bin/bash
###########
## genere rapport linter ruff
## nécessite d'avoir excute
## pip install ruff --user
## https://github.com/charliermarsh/ruff
###########
#source /home/userdev/env/bin/activate
ruff *py > ruff-report.txt
cat ruff-report.txt

