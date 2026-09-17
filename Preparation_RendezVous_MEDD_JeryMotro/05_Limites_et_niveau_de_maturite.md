---
title: Limites et niveau de maturité — JeryMotro
---
# Limites et niveau de maturité

> [!important] Pourquoi cette note existe
> Elle permet de répondre précisément aux questions difficiles sans présenter comme opérationnelle une fonction qui est seulement prévue ou partiellement validée.

## 1. Principe de classification

### 🟢 Démontrable

Fonction visible dans la version actuelle et pouvant être montrée pendant le rendez-vous.

### 🟡 À valider davantage

Fonction présente ou partiellement testée mais qui doit être évaluée sur davantage de données ou dans des conditions réelles.

### 🟠 Dépendante d’une intégration

Fonction nécessitant des identifiants, services externes ou données qui ne sont pas toujours disponibles dans l’environnement de démonstration.

### 🔵 Perspective

Fonction décrite dans la conception mais qui ne doit pas être présentée comme une capacité actuelle sans vérification du code et de l’environnement.

## 2. Données

La qualité des résultats dépend de la qualité, fraîcheur, couverture et disponibilité des données.

FIRMS fournit des **détections de feux actifs**. Une non-détection ne permet pas à elle seule de conclure à l’extinction.

## 3. Machine Learning

Le score ML est un indicateur. Il doit être évalué avec des données de validation adaptées.

> [!warning]
> Ne jamais annoncer une « précision de X % » si cette valeur n’a pas été calculée et documentée sur un jeu de test représentatif.

## 4. HDBSCAN / regroupement

Le regroupement dépend des paramètres spatiaux, temporels et de la densité des données. Des données trop rares peuvent limiter la qualité du regroupement.

## 5. Automatisation

L’architecture prévoit des workflows automatisés. Pour chaque démonstration, vérifier que la collecte, le traitement et les services externes nécessaires sont réellement disponibles.

## 6. Alertes

Les canaux prévus comprennent email, SMS et WhatsApp. Leur fonctionnement réel dépend de la configuration des fournisseurs et des credentials disponibles.

## 7. Chat IA / RAG

Le Chat IA dépend des workflows n8n et des services de données/modèle associés. Ne pas présenter le Chat comme un moteur entièrement contenu dans FastAPI.

## 8. Prédiction J+1 / Deep Learning

Les anciennes notes de conception décrivent un objectif de prédiction spatio-temporelle par Deep Learning. Cette vision doit être distinguée des fonctions actuellement déployées et validées.

## 9. Formulation recommandée

> « Le prototype démontre la faisabilité de plusieurs briques. La prochaine étape consiste à mesurer et valider les performances dans des conditions représentatives avec des données et observations adaptées. »
