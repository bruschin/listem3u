#!/bin/bash
#################
# Creer la liste des fichiers audios dans les ss-repertoires 
# de P:\Morceaux_choisis par defaut
# par lecture des fichiers m3u dans les sous répertoires
# https://github.com/koalaman/shellcheck
#################
# shellcheck disable=SC2034  # Unused variables left for readability
Version="[BN 11-03-2026 V1.0.3]"
Hostref="MiniGeekom13"
Repertoire_travail="/d/Morceaux_choisis"
Repertoire_automation="/c/Users/matel/Documents/GitHub/listem3u/automation"
Fichier_liste_tampon="liste.m3u"
Ancien_Fichier_liste_CTRL=""
Ancien_Fichier_liste_MP3=""
Fichier_liste="000-liste-$(date "+%d-%m-%Y")_ctrl.m3u"
testmachine="$(hostname)"

# Prévu pour fonctionner uniquement sur MiniGeekom13
if [[ "${testmachine}" != "${Hostref}" ]]; then
	printf ">>>Pb. Prevu pour tourner uniquement sur %s .\n" "${Hostref}"
	exit 1
fi

# Le répertoire de travail est-il accessible ? on s'y rend, sinon on sort
cd "${Repertoire_travail}" 1>/dev/null 2>/dev/null || \
	{ printf ">>>Pb. %s inexistant.\n" "${Repertoire_travail}";  exit 1; }

Ancien_Fichier_liste_MP3=$(find . -mindepth 0 -maxdepth 1 -type f \
	-name "000-liste*.m3u")
	# SonarQube : Use '[[' instead of 'test' command for conditional tests. 
	# The '[[' construct is safer and more feature-rich.
	# if test  -z "${Ancien_Fichier_liste_MP3}"; then  => 
	# if [[ -z "${Ancien_Fichier_liste_MP3}" ]]
if [[ -z "${Ancien_Fichier_liste_MP3}" ]]; then
	echo ">>>Pb. Ancien fichier de production mp3, non trouvé ."
	exit 1
fi

Ancien_nbrficmp3_prod=$(grep -vc "^#" < "${Ancien_Fichier_liste_MP3}")

compteur=0
maxmodif=0
for ficla in $(find -L "${Repertoire_automation}" -mindepth 0 -maxdepth 1 \
										-type f -name "000-liste*ctrl.m3u"); do
	
	derniermodifici=$(stat --printf=%Y "${ficla}")
	
	if [[ "${compteur}" -eq 0 ]]; then
		maxmodif="${derniermodifici}"
		Ancien_Fichier_liste_CTRL="${ficla}"
	  (( compteur +=1 ))
	elif [[ "${derniermodifici}" -gt "${maxmodif}" ]]; then
	  \rm -f "${Ancien_Fichier_liste_CTRL}" 1>/dev/null 2>/dev/null && \
		  (( compteur -=1 ))
	  maxmodif="${derniermodifici}"
	  Ancien_Fichier_liste_CTRL="${ficla}" && (( compteur +=1 ))
	else
	  \rm -f "${ficla}" 1>/dev/null 2>/dev/null
	fi
done

if [[ "${compteur}" -gt 1 ]]; then
  echo ">>>Pb. Plusieurs fichier de contrôle ."
	exit 1
fi

if [[ -z "${Ancien_Fichier_liste_CTRL}" ]]; then
	echo "Ancien fichier de contrôle, non trouvé"
	exit 1
fi

Ancien_nbrficmp3_ctrl=$(grep -vc "^#" < "${Ancien_Fichier_liste_CTRL}")
#printf "Debug : Ancien_nbrficmp3_ctrl = %s" "${Ancien_nbrficmp3_prod}"

if [[ "${Ancien_nbrficmp3_prod}" = "${Ancien_nbrficmp3_ctrl}" ]]; then
	echo "Pas de changment on ne fait rien"
	exit 0
fi

## Il y a eu du changement !
# on récupère la liste des fichiers m3u dans sous-rep 001 à 0xx..
ficm3u=$(find . -mindepth 1 -maxdepth 2 -type f -name "*Playlist.m3u")
#printf "debug \n%s" "${ficm3u}"

# on remet à jour automation
for fic in ${ficm3u}; do
	lerepici="$(dirname "${fic}" | sed -e "s@./@@g" )"
	leficici="$(basename "${fic}")"
	meffic="${lerepici}/${leficici}"
	#printf "Debug: %s\n" "${meffic}"
	ctrlrep="${Repertoire_automation}/${lerepici}"
	if [[ -n "${lerepici}" ]] && [[ ! -d "${ctrlrep}" ]]; then
	  mkdir -p "${ctrlrep}" 1>/dev/null 2>/dev/null
		#printf "Debug: création %s\n" "${ctrlrep}"
	fi
	\cp -f "${fic}" "${Repertoire_automation}/${meffic}" || \
		{ echo "Pb copy ${meffic}"; exit 1; }
done

# on remet à jour le fichier de controle
playlist=$(find . -mindepth 0 -maxdepth 1 -type f -name "000*m3u")
\cp -f "${playlist}" "${Repertoire_automation}/${Fichier_liste}" || \
		{ echo "Pb copy ${fic}"; exit 1; }

echo "MAJ ! En conséquence, pensez à mettre à jour les lignes 33 et 34 " + \
"du fichier test_listem3u.py"
printf "Egalement le dossier automation, le nouveau fichier 
de contrôle est %s.\n" "${Repertoire_automation}/${Fichier_liste}"

exit 0