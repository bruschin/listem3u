#!/bin/bash
set -e

# --- CONFIGURATION ---
GITLAB_URL="https://git.meteo.fr"
PROJECT_ID="2915"                                 # Remplacez par l'ID de votre projet
BRANCH="releases"
TOKEN="glpat-X99VMxgXdDMEiswHe2Oj6W86MQp1OjkH.01.0w0i3p2rs"                        # Token avec droit 'read_api'
TARGET_DIR="/var/www/html/doc-projet"              # Racine de votre site web interne
TMP_ZIP="/tmp/artifacts.zip"

# 1. Téléchargement du dernier artéfact réussi de la branche cible via l'API GitLab
echo "Téléchargement de l'artéfact..."
curl --location --silent --header "PRIVATE-TOKEN: $TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/jobs/artifacts/$BRANCH/download?job=pages-generate" \
  --output "$TMP_ZIP"

# Vérification que le fichier téléchargé est un zip valide (évite d'écraser le site en cas d'erreur API)
if file "$TMP_ZIP" | grep -q "Zip archive data"; then
    echo "Artéfact valide reçu. Déploiement..."
    
    # 2. Création du dossier cible s'il n'existe pas
    mkdir -p "$TARGET_DIR"
    
    # 3. Désarchivage dans un dossier temporaire pour éviter les coupures de service
    TMP_EXTRACT="/tmp/sphinx_extract"
    rm -rf "$TMP_EXTRACT" && mkdir -p "$TMP_EXTRACT"
    unzip -q "$TMP_ZIP" -d "$TMP_EXTRACT"
    
    # 4. Synchronisation vers le répertoire web (les artéfacts conservent l'arborescence)
    # Dans le zip, le chemin est : build/html/*
    rsync -av --delete "$TMP_EXTRACT/build/html/" "$TARGET_DIR/"
    
    # 5. Nettoyage
    rm -f "$TMP_ZIP"
    rm -rf "$TMP_EXTRACT"
    echo "Mise à jour de la documentation réussie."
else
    echo "Erreur : Le fichier téléchargé n'est pas une archive valide (Vérifiez le token ou le statut du pipeline)."
    rm -f "$TMP_ZIP"
    exit 1
fi
