#################
# Creer la liste des fichiers audios dans les ss-repertoires 
# de P:\Morceaux_choisis par defaut
# par lecture des fichiers m3u dans les sous répertoires
# https://github.com/koalaman/shellcheck
#################
# shellcheck disable=SC2034  # Unused variables left for readability
Version="[BN 06-02-2026 V1.0.0]"
Hostref="MiniGeekom13"
Repertoire_travail="/d/Morceaux_choisis"
Repertoire_automation="/c/Users/matel/Documents/GitHub/listem3u/automation"
Fichier_liste_tampon="liste.m3u"
Fichier_liste="000-liste-$(date "+%d-%m-%Y")_ctrl.m3u"

testmachine="$(hostname)"

if test "${testmachine}" != "${Hostref}"; then
  echo "Prevu pour tourner uniquement sur ${Hostref}."
  exit 1
fi

cd "${Repertoire_travail}" || { echo "${Repertoire_travail} inexistant"; \
                                exit 1; }

ficm3u=$(find . -mindepth 1 -maxdepth 2 -type f -name "*Playlist.m3u")
#printf "debug \n%s" "${ficm3u}"

for fic in ${ficm3u}; do
  \cp -f "${fic}" "${Repertoire_automation}/${fic}" || \
    { echo "Pb copy ${fic}"; exit 1; }
done

playlist=$(find . -mindepth 0 -maxdepth 1 -type f -name "000*m3u")
\cp -f "${playlist}" "${Repertoire_automation}/${Fichier_liste}" || \
    { echo "Pb copy ${fic}"; exit 1; }