---
title: Guide données et IA — JeryMotro
---
# Données et IA — explication simple

## FIRMS

**NASA FIRMS** fournit des observations satellitaires de feux actifs.

À expliquer simplement :

> « Le satellite observe une signature correspondant à une activité thermique ; JeryMotro exploite cette observation comme une donnée d’entrée. »

## MODIS et VIIRS

Ce sont des instruments/capteurs satellitaires utilisés pour produire des détections de feux actifs. Ils n’ont pas exactement la même résolution ni les mêmes caractéristiques.

## FRP

**Fire Radiative Power (FRP)** est un indicateur lié à l’énergie radiative du feu.

À l’oral :

> « Le FRP donne une indication de l’intensité radiative observée. »

## Clustering

Le clustering consiste à regrouper des observations proches selon des critères spatiaux et temporels.

> « Au lieu de regarder chaque point séparément, on cherche à identifier un événement cohérent. »

## HDBSCAN

HDBSCAN est une méthode de clustering basée sur la densité. Elle est intéressante lorsque les groupes n’ont pas nécessairement une forme ou une taille fixe.

## Score de risque

Le score résume l’analyse de plusieurs variables. Il ne faut pas le présenter comme une mesure directe de la réalité du terrain.

## XGBoost

XGBoost est un algorithme de Machine Learning adapté aux données tabulaires.

Dans JeryMotro, le microservice ML actuel utilise notamment XGBoost pour produire un score de dangerosité.

## RAG

RAG signifie **Retrieval-Augmented Generation**.

Principe :

```text
Question
   ↓
Recherche d’informations pertinentes
   ↓
Contexte
   ↓
Modèle IA
   ↓
Réponse
```

Dans JeryMotro, le workflow conversationnel est orchestré par n8n.

## Différence ML / DL

- **ML** : analyse de variables structurées et production d’un score.
- **DL** : modèles neuronaux pouvant notamment traiter des données complexes spatio-temporelles.

Les anciennes notes de conception décrivent une ambition DL/ConvLSTM pour la prédiction J+1. Il faut distinguer cette conception de ce qui est effectivement déployé et validé aujourd’hui.

## Phrase à retenir

> « Les données satellitaires apportent l’observation, le traitement transforme les observations en événements, et le Machine Learning ajoute une couche d’analyse. »
