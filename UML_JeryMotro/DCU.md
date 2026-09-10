# Diagramme de cas d'utilisation — JeryMotro

## Système

**JeryMotro**

## Acteurs

- **Visiteur**
- **Utilisateur Standard**
- **Utilisateur Premium**
- **Administrateur**

## Généralisation entre acteurs

- `Utilisateur Standard` **--|>** `Visiteur`
- `Utilisateur Premium` **--|>** `Utilisateur Standard`
- `Administrateur` **--|>** `Utilisateur Premium`

Les acteurs spécialisés héritent des fonctionnalités de l'acteur général.

## Cas d'utilisation par acteur

### Visiteur

- Créer un compte
- Consulter la carte des feux
- Consulter les feux actifs

### Utilisateur Standard

En plus des fonctionnalités héritées du Visiteur :

- S'authentifier
- Consulter les statistiques
- Dialoguer avec le Chat IA
- Gérer les alertes
- Recevoir les alertes e-mail

### Utilisateur Premium

En plus des fonctionnalités héritées de l'Utilisateur Standard :

- Définir une zone prioritaire
- Exporter les données
- Recevoir les alertes SMS et WhatsApp

### Administrateur

En plus des fonctionnalités héritées de l'Utilisateur Premium :

- Collecter les données
- Générer les prédictions de risque
- Regrouper les détections
- Mettre à jour le statut des feux
- Déclencher les alertes

## Relations entre cas d'utilisation

Les fonctionnalités nécessitant une authentification utilisent le cas d'utilisation `S'authentifier` :

- `Consulter les statistiques` **<<include>>** `S'authentifier`
- `Dialoguer avec le Chat IA` **<<include>>** `S'authentifier`
- `Gérer les alertes` **<<include>>** `S'authentifier`
- `Recevoir les alertes e-mail` **<<include>>** `S'authentifier`
- `Recevoir les alertes SMS et WhatsApp` **<<include>>** `S'authentifier`
- `Définir une zone prioritaire` **<<include>>** `S'authentifier`
- `Exporter les données` **<<include>>** `S'authentifier`

La réception d'une alerte suppose au préalable qu'une alerte ait été configurée et activée par l'utilisateur. Cette dépendance est représentée par :

- `Recevoir les alertes e-mail` **<<include>>** `Gérer les alertes`
- `Recevoir les alertes SMS et WhatsApp` **<<include>>** `Gérer les alertes`

## Principes de modélisation retenus

Le diagramme de cas d'utilisation reste volontairement centré sur les acteurs et les services fonctionnels offerts par JeryMotro.

Les bases de données, les services techniques et les mécanismes internes ne sont pas représentés ici. Les détails du pipeline de traitement, du clustering et des communications avec les services externes seront décrits dans les diagrammes d'activité, de séquence et d'architecture.
