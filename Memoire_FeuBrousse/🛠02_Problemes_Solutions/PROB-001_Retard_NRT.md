# 🛠️ PROB-001 — Décalage NRT (0.5–6h)
#JeryMotro #Problem #Solution #FIRMS
[[Glossaire_Tags]] | [[00_INDEX]]

| Champ | Valeur |
|-------|--------|
| **ID** | PROB-001 |
| **Priorité** | 🔴 Haute |
| **Statut** | ✅ Solution identifiée |

## Description
Les données FIRMS sont publiées avec 0,5 à 6h de délai selon le capteur. En saison sèche Madagascar, un feu peut parcourir plusieurs km en 3h.

## Solutions

**Solution 1 — Prédiction ML J+1 (priorité)** : JeryMotroNet XGBoost + ConvLSTM anticipe les zones à risque 24h à l'avance → [[04_JeryMotroNet]]

**Solution 2 — Collecte 30 min via n8n** : Pipeline automatisé toutes les 30 min → données fraîches dès publication → [[11_Automatisation_n8n]]

**Solution 3 — Multi-capteurs** : VIIRS SNPP + VIIRS NOAA21 + MODIS = 3 passages/heure → délai réduit à ~20–40 min

## Pour le jury/mémoire
> "Ce projet ne supprime pas le délai NRT (contrainte physique satellite). Il le contourne par la prédiction ML et le minimise par la collecte multi-capteurs toutes les 30 min."

| Date | Action |
|------|--------|
| 2026-01-29 | Identifié (cours création d'entreprise) |
| 2026-02-23 | Solutions documentées |
