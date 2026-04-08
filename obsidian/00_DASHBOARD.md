# 🔥 JeryMotro Platform — Dashboard Principal
#JeryMotro #MemoireL3 #Avancement #Milestone
[[Glossaire_Tags]] | [[00_INDEX]]

> **Plateforme intelligente de détection et d'alerte des feux de brousse à Madagascar**
> Mémoire L3 Génie Logiciel | 23/02/2026 → 23/05/2026

---

## 📊 PROGRESSION GLOBALE

| Phase | Semaines | Progression | Statut |
|-------|----------|-------------|--------|
| 🏗️ Fondation | S1–S4 | <progress value="4" max="4"></progress> `4/4 sem` | ✅ Terminé |
| 🔬 Modélisation | S5–S8 | <progress value="1" max="4"></progress> `1/4 sem` | 🔄 En cours |
| 🎯 Finalisation | S9–S12 | <progress value="0" max="4"></progress> `0/4 sem` | ⬜ À venir |

**Semaine courante :** `S5-S6 / S12`
**Semaines restantes :** `~6 semaines`
**Dernière mise à jour :** `30/03/2026`

---

## 🗓️ GANTT — PLANNING S1→S12

```mermaid
gantt
    title JeryMotro Platform — Planning 3 mois
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    section 🏗️ Fondation
    S1 Infrastructure & Setup         :s1, 2026-02-23, 7d
    S2 Collecte automatisée n8n       :s2, 2026-03-02, 7d
    S3 EDA Complète                   :s3, 2026-03-09, 7d
    S4 Feature Eng. + HDBSCAN         :s4, 2026-03-16, 7d

    section 🔬 Modélisation
    S5-S6 JeryMotroNet XGB+ConvLSTM   :s56, 2026-03-23, 14d
    S7 FastAPI + Frontend démarrage   :s7, 2026-04-06, 7d
    S8 Frontend complet + RAG         :s8, 2026-04-13, 7d

    section 🎯 Finalisation
    S9-S10 Alertes + Tests E2E        :s910, 2026-04-20, 14d
    S11 Déploiement + Optionnel       :s11, 2026-05-04, 7d
    S12 Mémoire + Soutenance          :s12, 2026-05-11, 12d
```

---

## ✅ STATUT PAR COMPOSANT

| Composant | Priorité | Progression | Statut |
|-----------|----------|-------------|--------|
| 🐳 Docker Infrastructure | Must | <progress value="8" max="10"></progress> | ✅ Opérationnel |
| ⚡ FastAPI Backend | Must | <progress value="5" max="10"></progress> | 🔄 En cours |
| 🤖 JeryMotroNet XGBoost | Must | <progress value="2" max="10"></progress> | 🔄 En cours (V2) |
| 🧠 JeryMotroNet ConvLSTM | Must | <progress value="1" max="10"></progress> | 🔄 En cours |
| 🔵 HDBSCAN Clustering | Must | <progress value="8" max="10"></progress> | ✅ Validé |
| ⚙️ Feature Engineering | Must | <progress value="6" max="10"></progress> | ✅ V2 (+GEE Contexte) |
| 🌍 GEE Enrichissement | Must | <progress value="4" max="10"></progress> | 🔄 Intégration en cours |
| 🖥️ Frontend React | Must | <progress value="0" max="10"></progress> | ⬜ S7 |
| ⚙️ n8n Automatisation | Must | <progress value="7" max="10"></progress> | ✅ Actif (30min) |
| 🧠 RAG ChromaDB + Groq | Must | <progress value="3" max="10"></progress> | 🔄 En cours |
| 🔔 Système Alertes | Must | <progress value="2" max="10"></progress> | ⬜ S9 |
| 🧪 Tests E2E | Must | <progress value="0" max="10"></progress> | ⬜ S9-S10 |
| 📄 Mémoire L3 | Must | <progress value="1" max="10"></progress> | ⬜ S12 |

> [!tip] Mettre à jour la valeur `value` (0→10) de chaque barre chaque semaine

---

## 🏆 MÉTRIQUES CIBLES (Must Hit pour la soutenance)

| # | Métrique | Cible | Actuel | Statut |
|---|----------|-------|--------|--------|
| M1 | Recall petits feux XGBoost vs NASA | **+25%** | — | ⬜ |
| M2 | AUC-ROC XGBoost | **≥ 0.88** | — | ⬜ |
| M3 | F1-Score XGBoost | **≥ 0.80** | — | ⬜ |
| M4 | MAE ConvLSTM carte J+1 | **< 0.15** | — | ⬜ |
| M5 | Latence pipeline complet | **< 5 min** | — | ⬜ |
| M6 | Latence alerte post-FIRMS | **< 30 min** | — | ⬜ |
| M7 | Silhouette HDBSCAN | **> 0.50** | — | ⬜ |
| M8 | Coverage tests FastAPI | **≥ 60%** | — | ⬜ |
| M9 | Latence endpoint FastAPI | **< 200ms** | — | ⬜ |

> [!info] Mettre à jour la colonne **Actuel** après chaque mesure (S6, S9, S10)

---

## 📦 LIVRABLES FINAUX — 23/05/2026

- [x] **L1** — Cahier des Charges final (Markdown Obsidian) ✅ 2026-03-11
- [x] **L1b** — Architecture V2 (Pipeline GEE + Stratégie données 2021-2026) ✅ 2026-03-30
- [ ] **L2** — Repo GitHub `jery-motro-platform` complet + README
- [x] **L3a** — `docker-compose up` partiel (API + DB + n8n) ✅ 2026-03-26
- [ ] **L3** — `docker-compose up` fonctionnel complet (5 services)
- [ ] **L4** — FastAPI déployée + Swagger UI (URL publique Railway/Render)
- [ ] **L5** — Frontend déployé sur Vercel (URL publique)
- [ ] **L6** — Modèle JeryMotroNet (XGBoost V2 + ConvLSTM) + rapport métriques PDF
- [ ] **L7** — Vidéo démo 3 minutes (MP4)
- [ ] **L8** — Mémoire L3 complet (PDF)
- [ ] **L9** — Présentation soutenance (PowerPoint)

<progress value="2" max="9"></progress> **`2 / 9 livrables complétés`**

---

## 🔑 CLÉS API — Statut d'obtention

| Service | Où obtenir | Statut |
|---------|-----------|--------|
| NASA FIRMS MAP_KEY | `firms.modaps.eosdis.nasa.gov` | ✅ Obtenue — en production |
| NASA Earthdata Token | `earthdata.nasa.gov` | ✅ Disponible |
| Groq API `gsk_...` | `console.groq.com` | ✅ Fournie |
| Google Earth Engine | Compte académique gratuit | ⬜ À créer (S5) — nécessaire GEE V2 |
| Twilio Sandbox | `twilio.com` | ⬜ À créer (S9) |

---

## ⚠️ RISQUES ACTIFS

```mermaid
pie title Exposition aux risques (probabilité × impact)
    "Décalage NRT FIRMS" : 30
    "GPU insuffisant ConvLSTM" : 25
    "Temps U-Net optionnel" : 20
    "Décision React/Flutter" : 15
    "Twilio sandbox" : 10
```

| Risque | Prob. | Impact | Mitigation | Statut |
|--------|-------|--------|------------|--------|
| Décalage NRT 0.5–6h | 🔴 Haute | Moyen | Prédiction ML 48h + collecte 30min | ⬜ Surveiller |
| GPU insuffisant ConvLSTM | 🟠 Moy. | Élevé | Google Colab T4 gratuit | ⬜ Préparer |
| Temps U-Net insuffisant | 🔴 Haute | Faible | Classé Optionnel — ne bloque pas | ✅ Géré |
| n8n cloud limite gratuite | 🟢 Faible | Faible | n8n self-hosted via Docker | ✅ Géré |
| Twilio sandbox expiration | 🟢 Faible | Faible | Email prioritaire absolue | ✅ Géré |

---

## 🧭 PIPELINE — Vue Rapide

```mermaid
flowchart LR
    A[🛰️ FIRMS API\nn8n 30min] --> B[🐍 Preprocessing\nPython]
    B --> C[🔵 HDBSCAN\nClustering]
    C --> D[🤖 JeryMotroNet\nXGBoost + ConvLSTM]
    D --> E[(🗄️ PostgreSQL\n+ ChromaDB)]
    E --> F[⚡ FastAPI\nREST]
    F --> G[🖥️ Frontend\nReact]
    F --> H[🔔 Alertes\nEmail + WhatsApp]
    F --> I[🧠 JeryMotro AI\nGroq + RAG]

    style A fill:#ff6b35,color:#fff
    style D fill:#7c4dff,color:#fff
    style F fill:#00bcd4,color:#fff
    style G fill:#4caf50,color:#fff
    style H fill:#f44336,color:#fff
```

---

## 🔗 NAVIGATION RAPIDE

| Document | Description |
|----------|-------------|
| [[01_Cahier_des_Charges]] | 📋 Référence absolue du projet |
| [[02_Architecture_Globale]] | 🏗️ Pipeline + Docker + FastAPI |
| [[03_Plan_Travail_3_Mois]] | 📅 Planning S1→S12 avec tâches cochables |
| [[04_JeryMotroNet]] | 🤖 Modèle ML/DL original |
| [[SUIVI_HEBDOMADAIRE]] | 📊 Suivi hebdomadaire KPIs |
| [[METRIQUES_CIBLES]] | 🎯 Tableau de bord métriques |

---

> [!warning] Règle obligatoire
> Ce dashboard doit être mis à jour **chaque lundi matin** avant de commencer à coder.
> 10 minutes max. C'est votre boussole pour la soutenance.

*Dernière mise à jour : 30/03/2026 — V2 (GEE Enrichissement + stratégie 2021-2026)*
