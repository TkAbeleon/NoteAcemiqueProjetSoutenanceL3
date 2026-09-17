---
title: Préparation rendez-vous MEDD — JeryMotro
tags:
  - JeryMotro
  - MEDD
  - rendez-vous
  - soutenance
---

# Préparation rendez-vous MEDD — JeryMotro

> [!important] Objet
> Espace de préparation au rendez-vous avec le **Ministère de l’Environnement et du Développement Durable (MEDD)**.
>
> Ces notes servent à distinguer la **vision du projet**, le **système réellement disponible aujourd’hui** et les **perspectives de collaboration**.

## Navigation

### Présenter le projet
- [[01_Fiche_non_technique_JeryMotro]] — document principal pour un décideur
- [[03_Guide_presentation_5_minutes]] — déroulé oral
- [[10_JeryMotro_en_30_secondes]] — présentation ultra-courte

### Répondre aux questions
- [[02_Fiche_technique_JeryMotro]] — architecture et fonctionnement réel
- [[04_Questions_reponses_MEDD]] — questions probables et réponses
- [[08_Guide_Donnees_et_IA]] — explications simples des notions techniques

### Démontrer et cadrer
- [[07_Guide_demo_JeryMotro]] — démonstration live
- [[05_Limites_et_niveau_de_maturite]] — ce qui est réel, partiel ou à valider
- [[06_Interet_pour_le_MEDD]] — intérêt et pistes de collaboration
- [[09_Feuille_de_route_apres_rendez_vous]] — passage du prototype à l’expérimentation
- [[11_Questions_a_poser_au_MEDD]] — questions à poser au ministère

## Règle de lecture

> [!warning] Ne pas mélanger conception et système actuel
> Les anciennes notes de conception dans `obsidian/` restent une **base solide pour comprendre l’intention du projet**, mais certaines informations ont évolué.
>
> Pour toute affirmation sur le fonctionnement actuel, donner priorité au **code, à la configuration actuelle et aux services réellement présents**.

## Sources principales utilisées

- Conception historique : [[01_Cahier_des_Charges]], [[02_Architecture_Globale]], [[04_JeryMotroNet]], [[05_HDBSCAN_Clustering]], [[07_JeryMotro_AI_RAG]], [[11_Automatisation_n8n]], [[12_Systeme_Alertes]], [[17_Fonctionnalite_Statut_Feu]], [[20_UML_JeryMotro_Platform]].
- Système actuel : dépôts `JeryMotro_WEB`, `JeryMotroBackend`, `ml_jerymotro`.
- Configuration backend : `.env.example` du backend.

## Phrase directrice

> **JeryMotro est un prototype de plateforme de surveillance et d’analyse des feux de végétation à Madagascar, qui transforme des détections satellitaires et des données complémentaires en informations cartographiques, analytiques et en mécanismes d’alerte.**
