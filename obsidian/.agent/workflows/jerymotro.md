---
description: JeryMotro - Expert Python ML/DL & FastAPI
---

# 🚀 JeryMotro Workflow

Ce workflow active les règles de développement pour le projet **JeryMotro Platform**.

## 🛡️ RÈGLES D'ALIGNEMENT

1.  **Expertise :** Agir en tant qu'expert Python ML/DL et FastAPI.
2.  **Stack :** Respecter strictement FastAPI (async), XGBoost, ConvLSTM et Docker.
3.  **Features :** Utiliser les features `diff_brightness`, `frp_log`, `local_hour`, `is_dry_season`.
4.  **Seuils :** Alerte si `risk_score > 0.7` ou `FRP > 50MW`.
5.  **RAG :** JeryMotro AI répond uniquement sur les données du projet.
6.  **Sécurité :** Aucun secret en dur (.env uniquement).
7.  **Swagger :** Documentation automatique obligatoire sur `/docs`.

## 📂 STRUCTURE DES DOSSIERS

- `api/` : Backend FastAPI
- `ml/` : Scripts d'entraînement et inférence
- `n8n/` : Automatisations
- `frontend/` : Interface utilisateur (React prioritaire)
- `docker-compose.yml` : Orchestration

## 🧪 VÉRIFICATION

- Toujours tester les endpoints avec `httpx` (async).
- Recall cible pour XGBoost : ≥ +25% vs NASA brut.
- MAE cible pour ConvLSTM : < 0.15.

---
En cas de doute, consulter `rules_jerymotro.md` dans le brain ou les fichiers `.md` de l'Obsidian vault.
