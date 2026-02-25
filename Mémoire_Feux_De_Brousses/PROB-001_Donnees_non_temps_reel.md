# 🛠️ PROB-001 — Données Satellites Non en Temps Réel
#FireProject #Problem #Solution #Risque #FIRMS #MODIS #VIIRS
[[Glossaire_Tags]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **ID** | PROB-001 |
| **Date découverte** | 2026-01-29 |
| **Source** | Cours Création d'Entreprise — commentaire Mme Larissa |
| **Priorité** | 🔴 Haute |
| **Statut** | ✅ Solutions identifiées |

---

## Description du problème

Les données FIRMS (MODIS/VIIRS) sont publiées en **Near Real-Time (NRT)** mais avec un décalage systématique :

| Capteur | Délai minimum | Délai maximum |
|---------|--------------|---------------|
| VIIRS SNPP | 30 min | 3h |
| VIIRS NOAA-20 | 30 min | 3h |
| MODIS Terra | 1h | 6h |
| MODIS Aqua | 1h | 6h |

**Conséquence concrète :** Un feu déclaré à 08h00 ne sera visible dans FIRMS qu'entre 08h30 et 14h00. En milieu sec (saison sèche Madagascar), un feu peut parcourir plusieurs kilomètres en 3h.

**Impact sur le projet :** Risque de retard d'alerte → diminution de la réactivité → augmentation de l'impact destructeur.

---

## Solutions proposées

### Solution 1 — Prédiction ML/DL (PRIORITÉ)

Anticiper les zones à risque **avant** que le feu se déclare.

- **Modèle :** XGBoost + LSTM sur historique 7 jours
- **Horizon :** 48–72h avant l'événement
- **Données :** Historique FIRMS + NDVI + (météo ERA5 si dispo)
- **Résultat :** Alertes préventives → mobilisation avant le feu
- **Référence :** [[TECH-002_XGBoost]] | [[TECH-004_LSTM_TimeSeries]]

### Solution 2 — Fusion Multi-capteurs

Réduire le délai en combinant plusieurs satellites.

| Stratégie | Réduction délai |
|-----------|----------------|
| VIIRS SNPP + VIIRS NOAA-20 + MODIS | Couverture quasi-continue |
| Sentinel-1 SAR (tout temps) | Détection même la nuit/nuages |
| Résultat combiné | Délai ramené à ~30–45 min |

### Solution 3 — Pipeline n8n Optimisé

- Polling API toutes les 30 minutes (pas quotidien)
- Dès nouvelles données disponibles → inférence immédiate
- Seuil d'alerte bas (0.6 au lieu de 0.7) en début de saison sèche
- **Référence :** [[07_Automatisation_n8n]]

### Solution 4 — Système de Priorité des Alertes

Classer les alertes par niveau d'urgence :

| Niveau | Critères | Action |
|--------|----------|--------|
| 🔴 CRITIQUE | FRP > 100MW + confidence > 80% | Alerte immédiate |
| 🟠 ÉLEVÉ | FRP 30–100MW + score ML > 0.8 | Alerte dans 30 min |
| 🟡 MODÉRÉ | Score ML 0.5–0.8 | Rapport quotidien |
| 🟢 FAIBLE | Score ML < 0.5 | Monitoring standard |

---

## Notes pour le jury

> "Ce projet ne prétend pas résoudre le délai NRT — c'est une contrainte physique des satellites. Il le **contourne** grâce à la prédiction ML/DL qui anticipe les événements avant leur occurrence."

---

## Historique

| Date | Action | Tag |
|------|--------|-----|
| 2026-01-29 | Problème identifié | #Problem |
| 2026-02-23 | Solutions documentées | #Solution |
| — | À tester S4–S8 | #Avancement |
