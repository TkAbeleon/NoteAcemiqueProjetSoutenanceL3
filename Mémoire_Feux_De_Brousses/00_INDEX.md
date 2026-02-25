# 🔥 FireProject — Index Principal
#FireProject #MemoireL3 #ThinkTank
[[Glossaire_Tags]]

> **Plateforme intelligente de suivi des feux de brousse et de la déforestation à Madagascar**
> IA classique + IA générative + Automatisation
> Soutenance L3 — Mme Larissa

---

## 🗺️ Navigation du Vault

### 📋 Documents Stratégiques
- [[01_Cahier_des_Charges]] — Cahier des charges complet
- [[02_Think_Tank]] — Vision, architecture, fondation du projet
- [[03_Plan_Travail_3_Mois]] — Planning semaine par semaine

### 🏗️ Architecture Technique
- [[04_Architecture_Globale]] — Schéma complet de la plateforme
- [[05_APIs_et_Donnees]] — Toutes les APIs et sources de données
- [[06_Pipeline_ML_DL]] — Modèles ML/DL, pipeline technique
- [[07_Automatisation_n8n]] — Workflows n8n

### 📊 Données & Datasets
- [[08_Dataset_FIRMS_MODIS]] — Dataset principal MODIS/VIIRS
- [[08_Dataset_FIRMS_VIIRS]] — Dataset VIIRS SNPP/NOAA
- [[08_Dataset_Sentinel2]] — Dataset Sentinel-2 ESA

### 🛠️ Problèmes & Solutions
- [[PROB-001_Donnees_non_temps_reel]] — Décalage NRT 0.5–6h
- [[PROB-002_Couverture_nuageuse]] — Nuages masquant les feux
- [[PROB-003_Manque_labels_terrain]] — Absence de ground truth

### 🧪 Techniques IA
- [[TECH-001_Random_Forest]] — Classification feu/non-feu
- [[TECH-002_XGBoost]] — Prédiction zones à risque
- [[TECH-003_CNN_Segmentation]] — Segmentation images satellites
- [[TECH-004_LSTM_TimeSeries]] — Séries temporelles
- [[TECH-005_UNet]] — Délimitation zones déforestées

### 📚 Références
- [[REF-001_NASA_FIRMS_API]] — Documentation API FIRMS
- [[REF-002_AFIS_System]] — Système AFIS Afrique du Sud
- [[REF-003_Copernicus_Sentinel]] — ESA Sentinel Hub

### 📅 Notes Quotidiennes
- [[DailyNote_Template]] — Template à copier chaque jour

### 🔧 Outils & Templates
- [[Glossaire_Tags]] — Tous les tags du projet
- [[Dataset_Template]] — Template dataset
- [[Techniques_Template]] — Template technique IA
- [[Probleme_Solution_Template]] — Template problème/solution
- [[References_Template]] — Template référence

---

## 📈 Tableau de Bord Avancement

| Phase | Période | Statut |
|-------|---------|--------|
| Phase 1 — Fondations | Mois 1 (S1–S4) | 🟡 En cours |
| Phase 2 — Développement | Mois 2 (S5–S8) | ⬜ À venir |
| Phase 3 — Finalisation | Mois 3 (S9–S12) | ⬜ À venir |
| Soutenance | Fin mois 3 | ⬜ À venir |

---

## 🔑 Informations Clés

| Élément | Valeur |
|---------|--------|
| Zone cible | Madagascar (43.0°E–50.5°E, 11.9°S–25.6°S) |
| Bounding Box FIRMS | `43.0,-25.6,50.5,-11.9` |
| Sources principales | MODIS NRT + VIIRS SNPP NRT + Sentinel-2 |
| Stack IA | Random Forest → XGBoost → CNN/U-Net → LSTM |
| Automatisation | n8n (self-hosted ou cloud) |
| IA Générative | Ollama (local) + Groq (API) |
| Budget initial | 0 Ar (ressources gratuites uniquement) |

---

*Dernière mise à jour : {{date}}*
