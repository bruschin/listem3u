#!/bin/bash
#################
# Creer la liste des fichiers audios dans les ss-repertoires 
# de P:\Morceaux_choisis par defaut
# par lecture des fichiers m3u dans les sous répertoires
# https://github.com/koalaman/shellcheck
#################
Version="[BN 12-04-2023 V1.2]" # shellcheck
Repertoire_travail="p:\Morceaux_choisis"
Fichier_liste_tampon="liste.m3u"
Fichier_liste="liste-$(date "+%d-%m-%Y").m3u"

cd "${Repertoire_travail}"
if test $? -ne 0; then
	echo "${Repertoire_travail} inexistant"
	exit 1
fi

if test -f "${Fichier_liste_tampon}"; then
	rm -f "${Fichier_liste_tampon}"
fi
if test -f  "${Fichier_liste}"; then
	rm -f "${Fichier_liste}"
fi

ficm3u=$(find . -mindepth 1 -maxdepth 2 -type f -print | grep "Playlist.m3u$")
#echo "test ${ficm3u}"
for fic in ${ficm3u}; do
	cat "${fic}" | LC_COLLATE=C sort --ignore-case >> "${Fichier_liste_tampon}"
	echo -e "\n" >> "${Fichier_liste_tampon}"
done
cat  "${Fichier_liste_tampon}" | \
grep -Ev -e "^[[:blank:]]*(#|$)" | \
LC_COLLATE=C sort --ignore-case > "${Fichier_liste}"
#sleep 4
rm -f  "${Fichier_liste_tampon}"
exit 0
