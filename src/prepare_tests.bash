#################
# Creer la liste des fichiers audios dans les ss-repertoires 
# de P:\Morceaux_choisis par defaut
# par lecture des fichiers m3u dans les sous répertoires
# https://github.com/koalaman/shellcheck
#################
# shellcheck disable=SC2034  # Unused variables left for readability
Version="[BN 14-02-2026 V1.0.2]"
Hostref="MiniGeekom13"
Repertoire_travail="/d/Morceaux_choisis1"
Repertoire_automation="/c/Users/matel/Documents/GitHub/listem3u/automation"
Fichier_liste_tampon="liste.m3u"
Ancien_Fichier_liste_CTRL=""
Ancien_Fichier_liste_MP3=""
Fichier_liste="000-liste-$(date "+%d-%m-%Y")_ctrl.m3u"
#FICCTRL = os.path.join(REPERTOIRE,"000-liste-12-02-2026_ctrl.m3u")
#NBRFICMP3 = 1175

testmachine="$(hostname)"

# Prévu pour fonctionner uniquement sur MiniGeekom13
if [[ "${testmachine}" != "${Hostref}" ]]; then
  echo "Prevu pour tourner uniquement sur ${Hostref}."
  exit 1
fi

# Le répertoire de travail est-il accessible ? on s'y rend, sinon on sort
cd "${Repertoire_travail}" 1>/dev/null 2>/dev/null || \
  { echo "${Repertoire_travail} inexistant";  exit 1; }
#if [[ "$?" -ne 0 ]]; then 
#  echo "${Repertoire_travail} inexistant"
#  exit 1
#fi

Ancien_Fichier_liste_MP3=$(find . -mindepth 0 -maxdepth 1 -type f \
  -name "000-liste*.m3u")
#printf "Debug : Ancien_Fichier_liste_MP3 = %s" "${Ancien_Fichier_liste_MP3}"

# SonarQube : Use '[[' instead of 'test' command for conditional tests. 
# The '[[' construct is safer and more feature-rich.
# if test  -z "${Ancien_Fichier_liste_MP3}"; then  => 
# if [[ -z "${Ancien_Fichier_liste_MP3}" ]]
if [[ -z "${Ancien_Fichier_liste_MP3}" ]]; then
  echo "Ancien fichier de production mp3, non trouvé"
  exit 1
fi
Ancien_nbrficmp3_prod=$(wc -l < "${Ancien_Fichier_liste_MP3}")
#printf "Debug : Ancien_nbrficmp3_prod = %s" "${Ancien_nbrficmp3_prod}"

Ancien_Fichier_liste_CTRL=$(find -L "${Repertoire_automation}" \
  -mindepth 0 -maxdepth 1 -type f -name "000-liste*ctrl.m3u")
#printf "Debug : Ancien_Fichier_liste_CTRL = %s" "${Ancien_Fichier_liste_CTRL}"

if [[ -z "${Ancien_Fichier_liste_CTRL}" ]]; then
  echo "Ancien fichier de contrôle, non trouvé"
  exit 1
fi
Ancien_nbrficmp3_ctrl=$(wc -l < "${Ancien_Fichier_liste_CTRL}")
#printf "Debug : Ancien_nbrficmp3_ctrl = %s" "${Ancien_nbrficmp3_prod}"

if [[ "${Ancien_nbrficmp3_prod}" = "${Ancien_nbrficmp3_ctrl}" ]]; then
  echo "Pas de changment on ne fait rien"
  exit 0
fi

## Il y a eu du changement !
# on récupère la liste des fichiers m3u dans sous-rep 001 à 012..
ficm3u=$(find . -mindepth 1 -maxdepth 2 -type f -name "*Playlist.m3u")
#printf "debug \n%s" "${ficm3u}"

# on remet à jour automation
for fic in ${ficm3u}; do
  \cp -f "${fic}" "${Repertoire_automation}/${fic}" || \
    { echo "Pb copy ${fic}"; exit 1; }
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
