# 🎓 Notes L3 – Tsiky Ny Antsa

Bienvenue dans mon vault Obsidian pour toutes mes notes de Licence 3.  
Ce dépôt contient toutes mes notes académiques, projets, références et idées prises tout au long de l'année universitaire.

## Description générale

Ce vault est organisé pour centraliser et suivre **toutes mes activités d'apprentissage** :

- Notes de cours et synthèses personnelles.
- Suivi de projets (comme le projet Feux de Brousse ou autres travaux pratiques).
- Problèmes rencontrés et solutions appliquées.
- Jeux de données, techniques et bibliothèques utilisées.
- Références et tutoriels pour faciliter l'étude et la recherche.
- Idées nouvelles et pistes pour approfondir mes connaissances.

## Objectif

L'objectif de ce vault est de :

1. Avoir un **point central** pour toutes mes notes de L3.
2. Faciliter la **recherche et l’organisation** grâce aux tags et liens internes.
3. Permettre un **suivi clair de mes projets et exercices**.
4. Servir de **référence rapide** pour les examens et travaux pratiques.

---

> Ce vault est conçu pour être évolutif : les nouvelles notes peuvent être ajoutées quotidiennement et reliées aux notes existantes via des tags et des liens internes.





C'est une très bonne approche. Pour vraiment maîtriser Obsidian, il faut mettre les mains dans le cambouis. Passons au **niveau 2** pour les trois extensions les plus puissantes. Voici les détails techniques et les astuces de "Power User" pour vous faire gagner un temps fou.

---

## 1. Dataview : Au-delà du simple tableau

Pour exploiter Dataview à 100 %, il faut comprendre deux concepts clés : les champs en ligne et les différents types d'affichage.

### A. Les champs en Ligne (Inline Fields)

Vous n'êtes pas obligé de tout mettre dans le bloc YAML tout en haut de votre note. Vous pouvez créer des données _n'importe où_ dans votre texte en utilisant `::`.

- **Exemple dans votre texte :** `Ce livre a été écrit par Auteur:: Victor Hugo et m'a coûté Prix:: 15€.`
    
- **Dans votre requête Dataview**, vous pourrez appeler les colonnes "Auteur" et "Prix" exactement comme si elles étaient dans le YAML.
    

### B. Les 4 formats magiques de Dataview

Remplacez le mot `TABLE` par un de ces trois autres mots selon vos besoins :

- `LIST` : Fait une simple liste à puces (idéal pour lister des liens).
    
- `TASK` : Va chercher **toutes les cases à cocher** (`- [ ]`) dispersées dans vos notes et les rassemble au même endroit.
    
- `CALENDAR file.ctime` : Crée un calendrier visuel basé sur la date de création de vos notes.
    

### C. Exemple d'une requête complexe (à copier-coller)

Voici comment filtrer, trier et regrouper :

Extrait de code

```
TABLE Auteur, Prix
FROM "Bibliothèque" OR #livre
WHERE Prix > 10
SORT Prix DESC
```

_(Cela affiche tous les livres de votre dossier "Bibliothèque" ou ayant le tag #livre, qui coûtent plus de 10€, classés du plus cher au moins cher)._

---

## 2. Templater : L'automatisation sans coder (ou presque)

Templater prend tout son sens quand il agit tout seul.

### A. Les "Folder Templates" (Modèles de dossier)

C'est la fonctionnalité la plus utile :

1. Allez dans les réglages de Templater.
    
2. Descendez jusqu'à **"Folder Templates"**.
    
3. Associez un dossier à un modèle (ex: Dossier `Clients` associé au modèle `Template_Client`).
    
4. **Résultat :** Dès que vous créez une nouvelle note dans le dossier "Clients", elle se remplit toute seule avec le bon modèle. Plus besoin de le lancer manuellement !
    

### B. Les commandes interactives

Ajoutez ceci dans vos modèles pour qu'Obsidian vous pose des questions lors de la création de la note :

- **Demander une info :** `<% tp.system.prompt("Quel est le nom du client ?") %>` (Obsidian ouvrira une petite fenêtre pour taper le nom).
    
- **Placer le curseur :** Mettez `<% tp.file.cursor(1) %>` là où vous voulez commencer à écrire. Dès que le modèle est appliqué, votre souris clignotera exactement à cet endroit.
    

---

## 3. Kanban : De la simple carte à la vraie note

Beaucoup utilisent Kanban juste pour faire des listes visuelles, mais c'est bien plus qu'un "post-it".

### A. Créer des notes depuis vos cartes

Si vous écrivez "Faire le rapport financier" sur une carte Kanban, ce n'est qu'un bout de texte.

1. Allez dans les réglages du plugin Kanban.
    
2. Activez **"Linked page metadata"** ou définissez un dossier par défaut pour les nouvelles notes.
    
3. Sur votre tableau Kanban, cliquez sur les trois petits points d'une carte et choisissez **"Create note from card"**.
    
4. **Résultat :** La carte devient un lien cliquable `[[Faire le rapport financier]]`, et une vraie note est générée dans votre coffre pour y taper vos détails.
    

### B. Les dates d'échéance (Due Dates)

Vous pouvez ajouter des dates sur vos cartes en tapant `@` suivi de la date (ex: `@2026-03-05`).

- **Astuce :** Dans les réglages Kanban, vous pouvez lier ces dates au plugin "Calendar" ou "Tasks" d'Obsidian pour voir vos échéances Kanban directement sur votre calendrier global.
    

---

**Souhaitez-vous que nous nous concentrions sur un de vos besoins précis ?** Par exemple : voulez-vous que je vous construise l'architecture complète d'un **CRM (gestion de clients)** ou d'un **Système de prise de notes d'étudiant** (Zettelkasten) utilisant ces outils ?
