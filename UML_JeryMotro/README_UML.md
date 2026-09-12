# UML JeryMotro — Dossier de travail

Ce dossier constitue l'espace de travail UML principal du projet JeryMotro.

## Référentiel de modélisation

Les diagrammes sont construits à partir du fonctionnement réel du système, en priorité du code backend/frontend. Les anciens diagrammes peuvent présenter un léger décalage et ne sont donc pas utilisés comme source de vérité lorsqu'ils contredisent le code.

## Chaînage de travail

```text
Code réel
   ↓
Règles de gestion
   ↓
Dictionnaire de données
   ↓
Diagramme de classes
   ↓
Cas d'utilisation / séquences / activités
```

## Documents principaux

- `Regles_de_gestion.md` — règles métier issues du backend réel.
- `Dictionnaire_de_donnees.md` — entités, attributs, types, contraintes et associations.
- `Diagramme_de_classes.plantuml` — modèle de classes persistant actuel.
- `DCU.plantuml` / `DCU.md` — diagramme et synthèse des cas d'utilisation.
- `Description textuel.md` — descriptions textuelles des cas d'utilisation.
- `DS01_...` à `DS16_...` — diagrammes de séquence.
- `DA01_...` à `DA16_...` — diagrammes d'activité.

## Principes importants

1. Ne pas inventer d'association sans clé étrangère ou justification métier vérifiable.
2. Ne pas transformer les composants techniques externes en classes métier : NASA FIRMS, n8n, Qdrant, service ML, WAHA et fournisseurs SMS restent dans les diagrammes d'architecture, de séquence ou d'activité.
3. `Prediction` est une entité persistée mais ne possède actuellement pas de FK vers `User`, `FireEvent` ou `FirmsFireDetection`.
4. `FirmsFireDetection.collection_run_id` existe mais n'est pas une FK déclarée vers `CollectionRun`; le diagramme de classes ne représente donc pas cette relation comme association forte.
5. Le pipeline automatique suit la collecte planifiée : collecte → traitement du risque → regroupement → statut → alertes.
6. Le Chat IA est orchestré par n8n ; le backend joue le rôle de reverse proxy et le modèle de Chat IA conserve le recours à la DB et à Qdrant.

## État du modèle

Le contenu de ce dossier est une **copie de travail académique** alignée sur le backend actuel. Les fichiers techniques du backend sous `Backend/UML/` restent la référence détaillée côté backend ; ce dossier rassemble les versions utilisées pour la construction et la soutenance UML.
