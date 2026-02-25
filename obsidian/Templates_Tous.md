# 🗂️ Templates — JeryMotro Platform
#JeryMotro #Reference
[[Glossaire_Tags]] | [[00_INDEX]]

> Ce fichier contient tous les templates à copier-coller. Créer un nouveau fichier pour chaque instance.

---

# TEMPLATE 1 — Daily Note

```markdown
# 📅 Daily Note — JeryMotro Platform
#JeryMotro #DailyNote #Avancement
[[Glossaire_Tags]] | [[00_INDEX]]

**Date :** {{date}}
**Semaine :** S___ / S12
**Phase :** Mois ___ (Fondation / Modélisation / Finalisation)
**Durée :** ___ h

---

## 1️⃣ Tâches réalisées ✅
-

## 2️⃣ Problèmes rencontrés 🔴
-
→ Si nouveau problème : créer PROB-XXX

## 3️⃣ Solutions appliquées 💡
-

## 4️⃣ Métriques / Résultats 📊

| Composant | Métrique | Valeur | Objectif |
|-----------|----------|--------|---------|
| | | | |

## 5️⃣ Idées 🚀
-

## 6️⃣ Prochain objectif
> **Demain :**
```

---

# TEMPLATE 2 — Dataset

```markdown
# 📊 Dataset — [NOM]
#JeryMotro #Dataset
[[Glossaire_Tags]] | [[00_INDEX]]

| Champ | Valeur |
|-------|--------|
| **Nom** | |
| **Source** | NASA / ERA5 / Autre |
| **Format** | CSV / GeoTIFF / JSON |
| **Bbox** | -25.5,43,-11.5,50 |
| **Période** | |
| **Coût** | Gratuit |
| **Date téléchargement** | {{date}} |

## Colonnes

| Colonne | Type | Description | Usage ML |
|---------|------|-------------|----------|
| | | | |

## Commande de téléchargement

\`\`\`python
# Code ici
\`\`\`

## Notes de nettoyage
-
```

---

# TEMPLATE 3 — Problème/Solution

```markdown
# 🛠️ PROB-XXX — [TITRE]
#JeryMotro #Problem #Solution
[[Glossaire_Tags]] | [[00_INDEX]]

| Champ | Valeur |
|-------|--------|
| **ID** | PROB-XXX |
| **Date** | {{date}} |
| **Priorité** | 🔴 Haute / 🟠 Moyenne / 🟢 Faible |
| **Statut** | 🔴 Ouvert / 🟡 En cours / ✅ Résolu |

## Description
[Contexte, origine, impact sur le projet]

## Solutions

### Solution 1 — [Nom]
[Description + approche technique + outils]

### Solution 2 — [Nom]
[Description]

## Solution retenue
> **Décision :** Solution ___ parce que...

## Pour le mémoire/jury
> [Comment formuler ce problème comme une force du projet]

| Date | Action |
|------|--------|
| {{date}} | Identifié |
```

---

# TEMPLATE 4 — Référence

```markdown
# 📚 REF-XXX — [TITRE]
#JeryMotro #Reference
[[Glossaire_Tags]] | [[00_INDEX]]

| Champ | Valeur |
|-------|--------|
| **Titre** | |
| **Source** | |
| **Lien** | |
| **Type** | API / Article / Documentation / Tutoriel |
| **Consulté** | {{date}} |

## Résumé
[2–3 phrases]

## Points clés retenus
-

## Application dans JeryMotro
[Comment utilisé concrètement dans le projet]

## Citation (mémoire)
\`\`\`
Auteur, A. (Année). Titre. Source. URL
\`\`\`
```
