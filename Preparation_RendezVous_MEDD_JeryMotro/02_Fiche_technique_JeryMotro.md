---
title: Fiche technique — JeryMotro
---
# JeryMotro — Fiche technique

> [!important] Règle
> Cette fiche décrit en priorité le **système actuel**. Les anciennes notes de conception servent de contexte, mais ne doivent pas être utilisées pour affirmer qu’une fonction est aujourd’hui opérationnelle.

## Architecture simplifiée

```text
Sources de données
      │
      ▼
Collecte / traitement
      │
      ▼
Backend FastAPI ─────► PostgreSQL
      │
      ├──────────────► Microservice ML XGBoost
      │
      └──────────────► n8n ─────► Chat IA / RAG
      │
      ▼
Frontend web
      │
      ├── Carte
      ├── Analyses / statistiques
      └── Alertes
             ├── Email
             ├── SMS
             └── WhatsApp
```

## Backend

Le backend est une API **FastAPI**. Il expose les données et orchestre les traitements nécessaires à l’application web.

La configuration actuelle prévoit notamment PostgreSQL, NASA FIRMS, le service ML, n8n, WAHA et un fournisseur SMS configurable.

## Données FIRMS

NASA FIRMS fournit des détections de feux actifs issues notamment de MODIS et VIIRS.

Une détection peut contenir notamment :

- latitude / longitude ;
- date et heure d’acquisition ;
- FRP ;
- brightness ;
- confiance ;
- satellite / instrument selon la source.

> [!warning] Limite importante
> FIRMS fournit des **détections**, pas une preuve directe d’extinction. L’absence de détection doit donc être interprétée avec prudence.

## Regroupement des détections

Les détections peuvent être regroupées en événements spatiaux et temporels. Le projet utilise/étudie **HDBSCAN** pour le clustering, avec une stratégie de repli lorsque le clustering n’est pas disponible.

## Machine Learning

Le dépôt `ml_jerymotro` contient un microservice de scoring basé sur **XGBoost**.

Le service reçoit des données tabulaires et produit notamment un score de dangerosité. Les variables peuvent inclure des informations thermiques, FRP, confiance et contexte environnemental selon le modèle utilisé.

> [!tip] À l’oral
> « Le modèle attribue un score ; il ne remplace pas l’observation terrain et ne constitue pas à lui seul une preuve. »

## Chat IA

Le Backend n’est pas le moteur conversationnel principal.

Le principe actuel est :

```text
Utilisateur
   ↓
Frontend
   ↓
Backend / proxy
   ↓
n8n
   ↓
RAG / données / modèle IA
   ↓
Réponse
```

n8n assure l’orchestration du workflow conversationnel et peut utiliser les données disponibles et la recherche documentaire/vectorielle selon la question.

## Alertes

Les canaux prévus sont :

- Email ;
- SMS ;
- WhatsApp.

Une alerte doit être liée à une configuration utilisateur appropriée. Les nouveaux contacts peuvent nécessiter une vérification OTP selon le canal et le fonctionnement actuel.

> [!warning] Ne pas présenter comme automatique à 100 %
> La chaîne complète d’automatisation et certaines intégrations doivent être décrites selon leur niveau réel de validation.

## Déploiement

Le projet actuel utilise plusieurs services. Pour la présentation technique, expliquer l’architecture réelle déployée plutôt qu’une architecture historique issue des premières notes de conception.

## Points techniques à savoir expliquer

### Pourquoi FIRMS ?

Parce qu’il fournit une source satellitaire structurée de détections de feux actifs.

### Pourquoi le clustering ?

Parce qu’une série de points proches dans l’espace et le temps peut représenter un même événement plutôt que plusieurs feux indépendants.

### Pourquoi XGBoost ?

Parce qu’il est adapté aux données tabulaires et permet de combiner plusieurs variables pour produire un score.

### Pourquoi une base de données ?

Pour conserver les détections, événements, résultats et informations nécessaires à l’historisation et à l’API.

### Pourquoi n8n ?

Pour orchestrer des workflows automatisés et intégrer différents services externes.

## À ne pas affirmer sans vérification

- qu’une collecte automatique fonctionne partout et en permanence ;
- qu’une connexion opérationnelle à toutes les sources prévues est déjà active ;
- qu’une prédiction J+1 par Deep Learning est actuellement opérationnelle ;
- qu’un score ML garantit qu’un feu est réel ;
- qu’une absence de détection signifie extinction certaine.
