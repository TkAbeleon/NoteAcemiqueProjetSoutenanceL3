# Repartition des Roles et Planning — StreamMG

**Document :** Organisation de l'equipe, responsabilites et planning previsionnel  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 1.0  
**Date :** Fevrier 2026

---

## 1. Contexte de la repartition

Le projet StreamMG est realise par une equipe de trois etudiants, chacun menant simultanement un memoire de licence individuel de grande envergure. Cette contrainte structurelle est le facteur determinant de la repartition des roles : chaque attribution de tache doit etre calibree pour etre realiste dans les plages de temps disponibles entre les engagements principaux de chaque membre, tout en valorisant les competences reelles et actuelles de chacun.

La repartition a ete construite autour de trois principes. Le premier est l'alignement competences-role : personne n'est place en position de devoir apprendre une technologie entierement nouvelle pour realiser sa part du projet. Le second est la protection des memoires principaux : la charge de travail sur StreamMG est calibree pour ne pas empieter de maniere critique sur les delais des memoires individuels. Le troisieme est la complementarite : les roles ne sont pas cloisonnes, ils se recoupent sur les aspects transversaux (securite, integration, revue de code) pour favoriser la coherence de l'ensemble.

---

## 2. Profils des membres de l'equipe

### Membre 1 — Developpeur Full-Stack

**Memoire individuel principal :** Conception d'une plateforme collaborative de creation et de valorisation des idees de projets innovants, integrant des mecanismes de collaboration, de suivi d'avancement et de gestion de l'investissement.

**Competences techniques disponibles pour StreamMG :** Node.js, Express.js, React, React Native, Expo, Git, MongoDB/Mongoose, architecture REST, authentification JWT. Ces competences sont directement reutilisables sans courbe d'apprentissage supplementaire significative.

**Charge estimee sur StreamMG :** 40 % de la charge globale du projet.

### Membre 2 — Ingenieur Donnees et Tests

**Memoire individuel principal :** Systeme de diagnostic medical assiste, avec version web et mobile classique.

**Competences techniques disponibles pour StreamMG :** Python, Flask, MongoDB, logique de donnees, tests fonctionnels, Postman, scripts de migration et de population de base de donnees.

**Charge estimee sur StreamMG :** 35 % de la charge globale du projet.

### Membre 3 — Chef de Projet Fonctionnel

**Memoire individuel principal :** Plateforme intelligente de suivi des feux de brousse et de la deforestation a Madagascar, integrant les donnees satellitaires NASA MODIS et VIIRS, de l'IA classique, de l'IA generative et de l'automatisation. Ce memoire est techniquement le plus ambitieux et le plus chronophage des trois.

**Competences mobilisees sur StreamMG :** Analyse des besoins, conception fonctionnelle, redaction de documents techniques, maitrise des outils UML, Figma, Trello/Notion, PowerPoint. Le role evite deliberement toute responsabilite de developpement backend ou d'infrastructure, afin de preserver l'essentiel de l'energie cognitive pour le memoire principal.

**Charge estimee sur StreamMG :** 25 % de la charge globale du projet.

---

## 3. Tableau detaille des responsabilites

### Domaine Architecture et Infrastructure

Le Membre 1 est seul responsable de la definition de l'architecture globale du systeme (choix des technologies, structure des dossiers, configuration des environnements), de la configuration de Nginx en tant que reverse proxy, et de la mise en place du pipeline de deploiement (Railway pour le backend, Vercel pour le frontend web). Le Membre 2 participe a la revue de l'architecture du point de vue de la couche donnees. Le Membre 3 valide l'architecture par rapport aux fonctionnalites definies dans le cahier des charges.

### Domaine Backend — API REST

Le Membre 1 developpe l'integralite de l'API REST : routes, controllers, middlewares d'authentification et d'autorisation, configuration Multer pour les uploads, integration du SDK Stripe en mode test, et gestion du streaming des fichiers medias. Le Membre 2 valide les endpoints via la collection Postman et remonte les anomalies detectees. Le Membre 3 definit les specifications fonctionnelles de chaque endpoint (quelles donnees entrent, quelles donnees sortent, quels codes d'erreur) dans le cahier des charges.

### Domaine Base de Donnees

Le Membre 2 est responsable de la conception complete du schema de donnees MongoDB : definition des collections, des champs, des types, des validations, des valeurs par defaut et des contraintes d'unicite. Il est responsable de la creation des schemas Mongoose, de la mise en place des index pour les requetes les plus frequentes, et de la redaction des scripts de population initiale de la base de donnees (jeu de donnees de demonstration pour la soutenance). Le Membre 1 integre les modeles Mongoose dans le backend lors du developpement. Le Membre 3 valide que le modele de donnees supporte toutes les fonctionnalites definies dans le cahier des charges.

### Domaine Frontend — Application Expo

Le Membre 1 developpe les composants principaux de l'application Expo/React Native Web : navigation (expo-router), page d'accueil, catalogue, page de detail des contenus, lecteur video et audio (expo-av), mini-player persistant, formulaires d'authentification, et interface du tableau de bord administrateur. Le Membre 2 developpe les composants React Native pour l'affichage des statistiques dans le tableau de bord administrateur et participe au test d'integration frontend-backend. Le Membre 3 livre les specifications d'interface sous forme de maquettes Figma detaillees avant le debut du developpement de chaque ecran, et valide la conformite de l'implementation par rapport aux maquettes.

### Domaine Paiement Simule

Le Membre 1 integre les composants Stripe Elements cote frontend (formulaire de saisie de carte) et l'API Stripe cote backend (creation de PaymentIntent, verification de webhook). Le Membre 2 teste le flux complet de paiement simule (TF-PAY-01 a TF-PAY-04) et redige le rapport de validation. Le Membre 3 redige la section du cahier des charges decrivant le flux de paiement simule et prepare l'argument de soutenance justifiant ce choix (Stripe en mode test comme standard industrie pour les demonstrations academiques).

### Domaine Tests et Validation

Le Membre 2 est responsable de la redaction et de l'execution du plan de tests fonctionnels complet, de la creation et de la maintenance de la collection Postman documentant tous les endpoints de l'API, de la redaction du rapport de tests avec la matrice de traçabilite, et de la population de la base de donnees de demonstration avec des donnees realistes pour la soutenance. Le Membre 1 corrige les anomalies detectees par les tests. Le Membre 3 redige les scenarios utilisateur (base des cas de test) et valide les resultats des tests par rapport aux criteres d'acceptation definis dans le cahier des charges.

### Domaine Documentation et Memoire

Le Membre 3 est responsable de l'integralite de la documentation : cahier des charges, analyse du projet, scenarios utilisateur, rapport de repartition des roles, maquettes Figma, diagrammes UML (diagrammes de cas d'utilisation, diagrammes de sequences pour les flux principaux), redaction du memoire de licence accompagnant le projet, et preparation des slides de soutenance. Le Membre 1 redige la documentation technique de l'API (README du projet backend, annotations dans la collection Postman). Le Membre 2 redige la documentation de la base de donnees (description des collections et des index, guide de la collection Postman).

---

## 4. Planning previsionnel simplifie

Le planning est decrit en semaines relatives au debut du projet.

**Semaines 1 et 2 — Phase de conception.** Le Membre 3 finalise les maquettes Figma pour toutes les vues principales (accueil, catalogue, detail contenu, lecteur, profil, admin, paiement) sur web et mobile. Le Membre 2 livre la conception complete du schema MongoDB avec tous les champs et index. Le Membre 1 valide la faisabilite technique de l'architecture et initialise la structure des projets frontend et backend sur GitHub.

**Semaines 3 a 6 — Phase de developpement du backend.** Le Membre 1 developpe l'API REST par module, en commencant par l'authentification (semaine 3), puis le catalogue et l'historique (semaine 4), puis l'administration et l'upload (semaine 5), puis le paiement Stripe (semaine 6). Le Membre 2 teste chaque module apres livraison via Postman et remonte les anomalies.

**Semaines 3 a 6 — Phase de developpement du frontend (parallele).** Le Membre 1 developpe les ecrans Expo en parallele du backend, en commencant par la navigation et l'authentification, puis le catalogue, puis les lecteurs et le mini-player, puis l'administration et le formulaire de paiement.

**Semaines 7 et 8 — Phase de tests et de correction.** Le Membre 2 execute le plan de tests complet sur l'environnement de staging. Le Membre 1 corrige les anomalies critiques. Le Membre 3 effectue des tests utilisateur manuels sur les deux plateformes (web Chrome et mobile Expo Go sur smartphone physique).

**Semaine 9 — Phase de preparation de la soutenance.** Le Membre 3 finalise le memoire, les slides et la repetition de la demonstration. Le Membre 2 prepare le jeu de donnees de demonstration (contenus audio et video de taille reduite pour accelerer le chargement). Le Membre 1 securise le deploiement de staging pour la soutenance.

---

## 5. References bibliographiques

Brooks, F. P. (1975). *The Mythical Man-Month: Essays on Software Engineering*. Addison-Wesley. ISBN 978-0201835953.

Beck, K., & Fowler, M. (2000). *Planning Extreme Programming*. Addison-Wesley Professional. ISBN 978-0201710915.

Highsmith, J. (2009). *Agile Project Management: Creating Innovative Products* (2e ed.). Addison-Wesley Professional. ISBN 978-0321658395.

Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide*. Scrum.org. https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf
