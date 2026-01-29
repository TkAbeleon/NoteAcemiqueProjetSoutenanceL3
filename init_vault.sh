#!/bin/bash

# Nom du vault
VAULT="📂Memoire_FeuBrousse"

# Créer le dossier principal
mkdir -p "$VAULT"

# Définir les dossiers (avec icônes) et fichiers
declare -A FOLDERS_FILES=(
    ["🔥01_DailyNotes"]="DailyNote_Template.md"
    ["🛠02_Problemes_Solutions"]="Probleme_Solution_Template.md"
    ["📂03_Datasets"]="Dataset_Template.md"
    ["📊04_Techniques"]="Techniques_Template.md"
    ["📚05_References"]="References_Template.md"
    ["🏷06_Glossaire_Tags"]="Glossaire_Tags.md"
)

# Créer les dossiers et fichiers avec contenu
for folder in "${!FOLDERS_FILES[@]}"; do
    mkdir -p "$VAULT/$folder"
    file="$VAULT/$folder/${FOLDERS_FILES[$folder]}"

    case $folder in
        "🔥01_DailyNotes")
cat <<EOT > "$file"
# FireProject - Daily Note
#DailyNote #Avancement #Problem #Solution #Idea #Python #ML #DL #Dataset

Date: {{date}}
Durée: ___ h

## 1️⃣ Tâches réalisées / Avancement
-

## 2️⃣ Problèmes rencontrés 🔴
-

## 3️⃣ Solutions appliquées ✅
-

## 4️⃣ Idées 💡
-

## 5️⃣ Remarques générales / autres 📝
-
EOT
        ;;
        "🛠02_Problemes_Solutions")
cat <<EOT > "$file"
# FireProject - Problèmes et Solutions
#Problem #Solution

| Problème 🔴 | Solution ✅ | Statut | Date |
|-------------|------------|--------|------|
| CSV trop volumineux | Charger en batch / filtrer par zone | En cours | 2026-01-29 |
| Délai données NRT | Modèle prédictif propagation feu | À faire | 2026-01-30 |
EOT
        ;;
        "📂03_Datasets")
cat <<EOT > "$file"
# FireProject - Dataset
#Dataset #NASA #MODIS #VIIRS

Nom: FIRMS VIIRS NRT
Zone: Madagascar
Période: ___
Format: CSV
Lien: https://firms.modaps.eosdis.nasa.gov
Notes:
- Filtrer par latitude/longitude
- Vérifier doublons
- Ajouter date de téléchargement
EOT
        ;;
        "📊04_Techniques")
cat <<EOT > "$file"
# FireProject - Techniques
#ML #DL #Python #n8n

Nom de la technique: ___
Type: ML / DL / Python / Workflow
Description: ___
Usage dans le projet: ___
Notes / exemples: ___
EOT
        ;;
        "📚05_References")
cat <<EOT > "$file"
# FireProject - Références
#Reference #Article #Tutoriel #API

Titre: ___
Auteur / Source: ___
Lien: ___
Résumé: ___
Notes importantes: ___
EOT
        ;;
        "🏷06_Glossaire_Tags")
cat <<EOT > "$file"
# Glossaire des Tags - Projet Feux de Brousse

## Projet
- \`#FireProject\` : toutes les notes liées au projet mémoire feux de brousse Madagascar.

## Avancement
- \`#Avancement\` : tâches réalisées et progression du projet.
- \`#DailyNote\` : note quotidienne pour suivre les travaux effectués.

## Problèmes
- \`#Problem\` 🔴 : obstacles ou difficultés rencontrées.

## Solutions
- \`#Solution\` ✅ : solutions appliquées ou envisagées.

## Idées
- \`#Idea\` 💡 : nouvelles idées ou pistes d’amélioration.

## Données
- \`#Dataset\` 📂 : notes liées aux jeux de données.
- \`#NASA\`, \`#MODIS\`, \`#VIIRS\` : spécifie la source ou capteur.

## Techniques
- \`#ML\` 📊 : Machine Learning
- \`#DL\` 📊 : Deep Learning
- \`#Python\` 🐍 : scripts et notebooks Python
- \`#n8n\` ⚙️ : workflow et automatisation

## Références
- \`#Reference\` 📚 : toutes références bibliographiques ou tutoriels.
- \`#Article\` : articles scientifiques
- \`#Tutoriel\` : tutoriels vidéo ou texte
- \`#API\` : documentation API

## Astuces
- Ajouter les nouveaux tags dès création dans ce glossaire.
- Lier cette note partout via [[Glossaire_Tags]].
EOT
        ;;
    esac
done

echo "✅ Vault Obsidian '$VAULT' créé avec tous les templates et dossiers et icônes dans les noms !"
