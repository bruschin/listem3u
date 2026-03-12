#!/bin/bash
###########
## genere  index gitlab-pages mais aussi Doxyfile et sphinx
## en remplaçant 4 chaines :
## @RELEASE_VERSION@ @DATE@ @COMMIT@ @PIPELINE@
###########

export TZ="Europe/Paris"
REPTRAV="$(dirname "$0")"
REPLOG="rapports"
REPCONF="docs"
FICSORTIE="${REPLOG}/mefversions-rapport.txt"
VERSION_EN_COURS=""
FIC_VERSION_EN_COURS="${REPCONF}/versions_en_cours.dat"
LADATE="$(date "+%Y-%m-%d %H:%M")"
TAGRELEASE="@RELEASE_VERSION@"
TAGDATE="@DATE@"
TAGCOMMIT="@COMMIT@"
TAGPIPELINE="@PIPELINE@"
FIC_INDEX="${REPCONF}/index.html"
declare -a FICS_A_MODIFIER=(
"${FIC_INDEX}"
"${REPCONF}/Doxyfile"
"${REPCONF}/conf_github.py"
"${REPCONF}/conf_gitlab.py"
"${REPCONF}/sonar-project.properties"
"pyproject.toml"
)


function trouve_version(){
  ## trouve une version dans un fichier
  ##
  ## Args:
  ## -----
  ##  - lefichiersrc (chaine) = $FIC_VERSION_EN_COURS par defaut
  ##  - tagatrouver (chaine) = "^VERSION_PROJET=" par defaut
  ##
  ## Returns:
  ##  - s_version (chaine)
  ##
  s_version=""
  lefichiersrc=$1
  tagatrouver=$2
  if test -z "${lefichiersrc}"; then
    lefichiersrc="${FIC_VERSION_EN_COURS}"
  fi
  if test -z "${tagatrouver}"; then
    tagatrouver="^VERSION_PROJET="
  fi

  while read -r ligne
  do
    tampon="$(echo "${ligne}" | \
              awk  -F"${tagatrouver}" '{print $2}'| \
              tr -d "\n" || true)"
    if test -n "${tampon}"; then
      s_version="${tampon}"
      break
    fi    
  done <  <(grep -Ev "^[[:blank:]]*(#|$)" "${lefichiersrc}" || true)
  echo "${s_version}"
}

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

LECOMMIT=$1
LEPIPELINE=$2

cd "${REPTRAV}/.." || exit 1

echo "### $0 DEBUT ###"

if ! test -d "${REPLOG}"; then
  mkdir -p "${REPLOG}" 2>/dev/null
fi

exec 6>&1
exec >"${FICSORTIE}" 2>&1

echo "$0 : changement tag version dans divers fichiers"

## trouve version du projet
VERSION_EN_COURS="$(trouve_version \
                      "${FIC_VERSION_EN_COURS}" "^VERSION_PROJET=")"
if test -n "${VERSION_EN_COURS}"; then
  ## change TAGRELEASE de FIC_INDEX
  for ficachanger in "${FICS_A_MODIFIER[@]}"
  do
    nretour="$(change_tag "${TAGRELEASE}" "${VERSION_EN_COURS}" \
               "${ficachanger}")"
    if test "${nretour}" != "0"; then
      echo "Pb pour changer ${TAGRELEASE} dans ${ficachanger}"
    else
      echo "Changement ${TAGRELEASE} dans ${ficachanger}"
    fi
  done
else
  echo "Pb pour trouver la version du projet"
fi

## change TAGDATE de FIC_INDEX
nretour="$(change_tag "${TAGDATE}" "${LADATE}" "${FIC_INDEX}")"
if test "${nretour}" != "0"; then
  echo "Pb pour changer ${TAGDATE} dans ${FIC_INDEX}"
else
  echo "Changement ${TAGDATE} dans ${FIC_INDEX}"
fi

## change TAGCOMMIT de FIC_INDEX
nretour="$(change_tag "${TAGCOMMIT}" "${LECOMMIT}" "${FIC_INDEX}")"
if test "${nretour}" != "0"; then
  echo "Pb pour changer ${TAGCOMMIT} dans ${FIC_INDEX}"
else
  echo "Changement ${TAGCOMMIT} dans ${FIC_INDEX}"
fi

## change TAGPIPELINE de FIC_INDEX
nretour="$(change_tag "${TAGPIPELINE}" "${LEPIPELINE}" "${FIC_INDEX}")"
if test "${nretour}" != "0"; then
  echo "Pb pour changer ${TAGPIPELINE} dans ${FIC_INDEX}"
else
  echo "Changement ${TAGPIPELINE} dans ${FIC_INDEX}"
fi

exec 1>&6 6>&-

cat "${FICSORTIE}"
echo "### $0 FIN ###"
exit 0