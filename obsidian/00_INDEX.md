# 🔥 JeryMotro Platform — Index Principal
#JeryMotro #MemoireL3 #Soutenance
[[Glossaire_Tags]]

> **Plateforme intelligente de détection et d'alerte des feux de brousse à Madagascar**
> Pipeline complet : Collecte FIRMS → ML/DL (JeryMotroNet) → FastAPI → Frontend → Alertes
> **Mémoire L3 Génie Logiciel** | 23/02/2026 → 23/05/2026

---

## 🗺️ Navigation Vault

### 📋 Documents Fondateurs
- [[01_Cahier_des_Charges]] — Référence absolue du projet (v2.2)
- [[02_Architecture_Globale]] — Pipeline + Docker + FastAPI + Frontend
- [[03_Plan_Travail_3_Mois]] — Planning S1→S12 détaillé

### 🤖 Modèle & IA
- [[04_JeryMotroNet]] — Modèle original XGBoost + ConvLSTM
- [[05_HDBSCAN_Clustering]] — Clustering spatio-temporel (750m / 48h)
- [[06_Feature_Engineering]] — Features FIRMS + ERA5 + diff_brightness
- [[07_JeryMotro_AI_RAG]] — IA explicative Groq + ChromaDB (RAG)

### 🏗️ Infrastructure Technique
- [[08_Docker_Infrastructure]] — docker-compose complet
- [[09_FastAPI_Backend]] — API REST entre ML et Frontend
- [[10_Frontend_Decision]] — React vs Flutter (décision S2)
- [[11_Automatisation_n8n]] — Collecte 30min + orchestration
- [[12_Systeme_Alertes]] — Email + WhatsApp (Twilio Sandbox)

### 📊 Données
- [[13_Dataset_FIRMS_MODIS]] — MODIS NRT Madagascar
- [[14_Dataset_FIRMS_VIIRS]] — VIIRS SNPP + NOAA21 NRT
- [[15_Dataset_ERA5_GEE]] — Features climatiques Google Earth Engine

### 🛠️ Problèmes & Solutions
- [[PROB-001_Retard_NRT]] — Décalage 0.5–6h FIRMS
- [[PROB-002_Petits_feux_tavy]] — Sous-estimation < 1ha
- [[PROB-003_GPU_insuffisant]] — Entraînement DL sans GPU

### 📚 Références
- [[REF-001_NASA_FIRMS_API]] — Documentation API FIRMS
- [[REF-002_Groq_ChromaDB]] — IA Générative + RAG
- [[REF-003_Docker_FastAPI]] — Infrastructure technique

### 📅 Templates
- [[DailyNote_Template]]
- [[Dataset_Template]]
- [[Technique_Template]]
- [[ProblemeSolution_Template]]
- [[Reference_Template]]
- [[Glossaire_Tags]]

---

## 📈 Tableau de Bord

| Phase | Semaines | Objectif | Statut |
|-------|----------|---------|--------|
| Fondation | S1–S4 | Infra Docker + Données + EDA | 🟡 En cours |
| Modélisation | S5–S8 | JeryMotroNet + FastAPI + Frontend | ⬜ À venir |
| Finalisation | S9–S12 | Alertes + Tests + Mémoire | ⬜ À venir |

---

## 🔑 Constantes du Projet

| Élément | Valeur |
|---------|--------|
| Bbox Madagascar | `-25.5,43,-11.5,50` |
| Sources FIRMS | MODIS_NRT + VIIRS_SNPP_NRT + VIIRS_NOAA21_NRT |
| Fréquence collecte | Toutes les 30 minutes |
| Seuil alerte FRP | > 50 MW |
| Seuil alerte risque ML | > 0.70 |
| Latence pipeline cible | < 5 min |
| Latence alerte cible | < 30 min |
| Budget | 0 Ar (tout gratuit) |

---

*⚠️ Ce vault ne contient PAS de Think Tank ni de Business Canvas — projet purement académique L3 Génie Logiciel.*

*Dernière mise à jour : 23/02/2026*
