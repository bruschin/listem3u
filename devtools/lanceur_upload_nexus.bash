#!/bin/bash
###########
## upload package wheel vers Nexus
## ## [2026-02-18] BN V1.0.0

## pip install twine --user
## https://packaging.python.org/en/latest/tutorials/packaging-projects/
###########
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
REPBUILD="build/dist"
FICCONF="docs/.pypirc"
TAG_PROJECTNAME="%project-name%"
TAG_USERNAME="<nom_utilisateur>"
TAG_PASSWORD="<mot_de_passe>"
FICSORTIE="${REPLOG}/upload_nexus-rapport.txt"


function change_tag(){
	## Change une chaine non vide dans un fichier
	##
	## Args:
	## -----
	##  - tagachanger (chaine)
	##  - s_echange (chaine) si vide NOK
	##  - fichiersrc (chaine)
	##
	## Returns:
	##  - resultat (entier)  0 OK, 1 NOK
	resultat=1
	tagachanger=$1
	s_echange=$2
	fichiersrc=$3

	if test -n "${s_echange}"; then
		presence="$(grep -c "${tagachanger}" "${fichiersrc}" 2>/dev/null)"
		if test "${presence}" != "0"; then              
			sed -i -e "s/${tagachanger}/${s_echange}/g" "${fichiersrc}" 2>/dev/null
			if test $? -eq 0; then
				resultat=0
			fi
		fi
	fi
	echo "${resultat}"
}

### Principal
PROJECTNAME="$1"
USERNAME="$2"
PASSWORD="$3"

export TZ="Europe/Paris"

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPBUILD}"; then
	mkdir -p "${REPBUILD}" 2>/dev/null
fi

if ! test -d "${REPLOG}"; then
	mkdir -p "${REPLOG}" 2>/dev/null
fi


exec 6>&1
exec >"${FICSORTIE}" 2>&1

# securite en cas d'oubli dans pipeline CI/CD
if [[ -z "${PROJECTNAME}" ]]; then
	echo "Argument 1 null. Imprevu"
	exit 1
fi
# securite en cas d'oubli dans pipeline CI/CD
if [[ -z "${USERNAME}" ]]; then
	echo "Argument 2 null. Imprevu"
	exit 1
fi
# securite en cas d'oubli dans pipeline CI/CD
if [[ -z "${PASSWORD}" ]]; then
	echo "Argument 3 null. Imprevu"
	exit 1
fi

echo "$0 : Lanceur upload build vers Nexus"


nretour="$(change_tag "${TAG_PROJECTNAME}" "${PROJECTNAME}" "${FICCONF}")"
if test "${nretour}" != "0"; then
	echo "Pb pour changer ${TAG_PROJECTNAME} dans ${FICCONF}"
	exit 1
fi
echo "Changement ${TAG_PROJECTNAME} dans ${FICCONF}"


nretour="$(change_tag "${TAG_USERNAME}" "${USERNAME}" "${FICCONF}")"
if test "${nretour}" != "0"; then
	echo "Pb pour changer ${TAG_USERNAME} dans ${FICCONF}"
	exit 1
fi
echo "Changement ${TAG_USERNAME} dans ${FICCONF}"


nretour="$(change_tag "${TAG_PASSWORD}" "${PASSWORD}" "${FICCONF}")"
if test "${nretour}" != "0"; then
	echo "Pb pour changer ${TAG_PASSWORD} dans ${FICCONF}"
	exit 1
fi
echo "Changement ${TAG_PASSWORD} dans ${FICCONF}"

\cp -fv "${FICCONF}" "${HOME}/"

twine upload -r pypi-snapshots "${REPBUILD}/*whl" --verbose

exec 1>&6 6>&-

cat "${FICSORTIE}"

echo "### $0 FIN ###"
exit 0
