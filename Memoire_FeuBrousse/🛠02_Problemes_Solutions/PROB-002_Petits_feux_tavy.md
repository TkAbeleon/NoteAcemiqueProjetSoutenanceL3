# 🛠️ PROB-002 — Sous-estimation Petits Feux Tavy
#JeryMotro #Problem #Solution #FIRMS #ML
[[Glossaire_Tags]] | [[00_INDEX]]

| Champ | Valeur |
|-------|--------|
| **ID** | PROB-002 |
| **Priorité** | 🔴 Haute — Objectif central du mémoire |
| **Statut** | ✅ Solution = JeryMotroNet |

## Description
Les petits feux < 1 ha (pratique tavy = culture sur brûlis) sont systématiquement sous-estimés par le produit NASA brut car :
- FRP faible (< 10 MW)
- Confiance `low` ou absente dans FIRMS
- Durée courte (quelques heures)

**Impact :** Les zones les plus défavorisées (savane ouest, sud-ouest Madagascar) sont les moins bien couvertes.

## Solutions

**Solution principale — JeryMotroNet** : Entraîner sur données malgaches 2020–2025 avec labels semi-supervisés qui conservent les détections `low` confidence quand clustering spatial confirme le feu → +25% recall cible.

**Solution complémentaire — diff_brightness** : La feature `brightness - bright_t31` détecte les petits feux mieux que le FRP seul car elle capture la différence thermique même pour des feux faibles.

## Argument pour le mémoire
> "La contribution principale de JeryMotroNet est d'améliorer le recall des petits feux de brousse malgaches (+25% vs produit NASA brut) en combinant clustering spatial, feature engineering ciblé et modèle adapté au contexte local."

| Date | Action |
|------|--------|
| 2026-02-23 | Identifié comme problème central |
