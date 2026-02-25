# Repartition des Roles et Planning — StreamMG

**Document :** Organisation de l'equipe, responsabilites et planning previsionnel  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 2.0 (mise a jour)  
**Date :** Fevrier 2026

---

## 1. Contexte de la repartition

Le projet StreamMG est realise par une equipe de trois etudiants, chacun menant simultanement un memoire de licence individuel de grande envergure. La nouvelle repartition des roles, revisee par rapport a la version initiale, affecte chaque membre a un domaine technique dominant : le frontend pour le Membre 1, le backend pour le Membre 2, et la securite transversale combinee a la coordination fonctionnelle pour le Membre 3. Cette specialisation par domaine presente un double avantage : elle reduit les zones d'interference entre les membres et permet a chacun de produire un travail plus approfondi sur son perimetre, tout en maintenant des points d'integration collectifs reguliers.

La repartition a ete construite autour de trois principes. Le premier est l'alignement competences-role : chaque membre est place dans le domaine ou ses competences sont les plus solides ou les plus facilement mobilisables. Le second est la protection des memoires principaux : la charge de travail sur StreamMG est calibree pour ne pas empieter de maniere critique sur les delais des memoires individuels. Le troisieme est la complementarite : les roles se recoupent sur les aspects transversaux (securite, integration, revue de code) pour garantir la coherence de l'ensemble.

---

## 2. Profils des membres de l'equipe

### Membre 1 — Developpeur Frontend

**Memoire individuel principal :** Conception d'une plateforme collaborative de creation et de valorisation des idees de projets innovants, integrant des mecanismes de collaboration, de suivi d'avancement et de gestion de l'investissement.

**Domaine dans StreamMG :** Frontend — Application Expo/React Native Web (web et mobile depuis une base de code unique).

**Competences mobilisees :** React, React Native, Expo, expo-router, expo-av, zustand, TanStack Query, axios, nativewind, Stripe Elements (formulaire de paiement cote client), Figma (validation des maquettes en implementation).

**Charge estimee sur StreamMG :** 40 % de la charge globale du projet.

### Membre 2 — Developpeur Backend

**Memoire individuel principal :** Systeme de diagnostic medical assiste, avec version web et mobile classique.

**Domaine dans StreamMG :** Backend — API REST Node.js/Express, base de donnees MongoDB, gestion de l'upload des fichiers medias, integration Stripe cote serveur.

**Competences mobilisees :** Node.js, Express.js, MongoDB, Mongoose, Multer, music-metadata, fluent-ffmpeg, jsonwebtoken, bcryptjs, stripe SDK, Postman.

**Charge estimee sur StreamMG :** 35 % de la charge globale du projet.

### Membre 3 — Responsable Securite et Chef de Projet Fonctionnel

**Memoire individuel principal :** Plateforme intelligente de suivi des feux de brousse et de la deforestation a Madagascar, integrant les donnees satellitaires NASA MODIS et VIIRS, de l'IA classique, de l'IA generative et de l'automatisation.

**Domaine dans StreamMG :** Securite applicative transversale (frontend et backend), coordination fonctionnelle, documentation, et preparation de la soutenance.

**Competences mobilisees :** OWASP, JWT security, bcrypt, CORS, rate limiting, helmet, validation des entrees, tests de securite via Postman, redaction technique, UML, Figma, Trello/Notion.

**Charge estimee sur StreamMG :** 25 % de la charge globale du projet.

---

## 3. Tableau detaille des responsabilites

### Domaine Frontend (Membre 1, responsable)

Le Membre 1 est responsable de l'integralite de l'application Expo/React Native Web. Il developpe la navigation par expo-router, la page d'accueil avec la section hero et les contenus mis en avant, le catalogue avec filtres et recherche, les pages de detail des contenus, le lecteur video (expo-av), le lecteur audio avec mini-player persistant (expo-av, zustand pour l'etat global du player), les formulaires d'inscription et de connexion (en lien avec les endpoints backend definis par le Membre 2), la page de profil et d'historique, le tableau de bord administrateur (upload, liste des contenus, statistiques), et le formulaire de paiement simule via Stripe Elements.

Le Membre 1 est egalement responsable de la gestion de l'etat global via zustand (authStore et playerStore), de la configuration du client axios avec les intercepteurs de renouvellement automatique du JWT, et de la mise en place du Service Worker pour le mode hors-ligne via expo-PWA.

Le Membre 2 fournit au Membre 1 la documentation des endpoints de l'API (collection Postman) afin que l'integration frontend-backend soit possible de maniere independante, en parallele du developpement. Le Membre 3 fournit les maquettes Figma et les specifications fonctionnelles de chaque ecran avant le debut du developpement.

### Domaine Backend (Membre 2, responsable)

Le Membre 2 est responsable de l'integralite du serveur Node.js/Express : initialisation du projet, configuration d'Express, definition des routes et des controllers pour tous les modules (authentification, catalogue, historique, administration, paiement simule). Il est responsable de la conception et de l'implementation des modeles Mongoose, de la gestion de l'upload des fichiers medias via Multer, de l'extraction automatique des metadonnees audio via music-metadata, de l'integration du SDK Stripe pour la creation des PaymentIntents et la reception des webhooks, et de la configuration de la base de donnees MongoDB (index, schemas, population de donnees de demonstration).

Le Membre 2 est egalement responsable de la redaction de la documentation technique de l'API (collection Postman exportee, README du backend) et du rapport de tests fonctionnels des endpoints. Il travaille en etroite collaboration avec le Membre 3 pour integrer les mecanismes de securite dans chaque route et chaque controller.

### Domaine Securite Transversale (Membre 3, responsable)

Le Membre 3 est responsable de la definition et de la mise en oeuvre de la strategie de securite globale de l'application. Ce role est qualifie de transversal car la securite traverse a la fois le frontend (gestion des tokens en memoire, protection contre XSS) et le backend (authentification JWT, hachage des mots de passe, rate limiting, validation des entrees, CORS, en-tetes HTTP).

Concretement, le Membre 3 definit les specifications de securite dans le cahier des charges et verifie que le Membre 1 (frontend) et le Membre 2 (backend) les implementent correctement. Il redige les tests de securite (TF-SEC-01 a TF-SEC-04) et les execute lui-meme sur les environnements de developpement et de staging. Il est responsable de la configuration finale de Nginx (en-tetes Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, Content-Security-Policy) et de la mise en place du certificat SSL Let's Encrypt pour le deploiement de soutenance.

Le Membre 3 est aussi responsable de la coordination generale du projet : suivi de l'avancement via Trello, organisation des points de synchronisation hebdomadaires, gestion des dependances entre les taches du Membre 1 et du Membre 2, redaction de l'ensemble des documents du projet (present document, cahier des charges, analyse, scenarios utilisateur, architecture), et preparation de la soutenance (memoire, slides, repetition de la demonstration).

### Domaine Commun — Fournisseur de Contenu (acteur externe)

L'utilisateur de type Fournisseur de Contenu est un nouvel acteur integre dans la version 2.0 du projet. Il dispose d'un compte specifique (role "provider") qui lui donne acces a une interface d'upload de contenus simplifiee, distincte du tableau de bord administrateur complet. Le Membre 2 cree le role et les routes backend associees. Le Membre 1 developpe l'interface frontend. Le Membre 3 s'assure que les permissions du role "provider" sont correctement restreintes par rapport au role "admin" (un provider peut uploader et gerer ses propres contenus uniquement, pas ceux des autres providers ni les comptes utilisateurs).

---

## 4. Planning previsionnel simplifie

Le planning est organise en semaines relatives au debut du projet, avec les responsabilites clairement attribuees par membre.

Durant les semaines 1 et 2, qui constituent la phase de conception, le Membre 3 finalise les maquettes Figma pour toutes les vues principales sur web et mobile, et redige les specifications fonctionnelles detaillees de chaque ecran et de chaque endpoint. Le Membre 2 livre la conception complete du schema MongoDB et la liste des endpoints de l'API avec leurs signatures (URL, methode, body attendu, reponse). Le Membre 1 initialise la structure du projet Expo sur GitHub et valide la faisabilite de chaque ecran par rapport aux maquettes.

Durant les semaines 3 a 6, qui constituent la phase de developpement, le Membre 2 developpe le backend module par module dans cet ordre : authentification (semaine 3), catalogue et historique (semaine 4), administration et upload (semaine 5), paiement Stripe et role fournisseur (semaine 6). En parallele, le Membre 1 developpe le frontend en commencant par la navigation et l'authentification (semaine 3), puis le catalogue et la recherche (semaine 4), puis les lecteurs video/audio et le mini-player (semaine 5), puis l'administration, le formulaire de paiement et l'interface fournisseur (semaine 6). Le Membre 3, en parallele, configure les mecanismes de securite au fur et a mesure que les modules backend sont livres, et maintient la documentation a jour.

Durant les semaines 7 et 8, qui constituent la phase de tests, le Membre 3 execute le plan de tests fonctionnels et de securite complet sur l'environnement de staging. Le Membre 2 corrige les anomalies backend detectees. Le Membre 1 corrige les anomalies frontend.

La semaine 9 est dediee a la preparation de la soutenance. Le Membre 3 finalise le memoire et les slides. Le Membre 2 prepare le jeu de donnees de demonstration. Le Membre 1 valide le deploiement final et la fluidite de la demonstration sur les deux plateformes.

---

## 5. References bibliographiques

Brooks, F. P. (1975). *The Mythical Man-Month: Essays on Software Engineering*. Addison-Wesley. ISBN 978-0201835953.

Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide*. Scrum.org. https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf

Highsmith, J. (2009). *Agile Project Management: Creating Innovative Products* (2e ed.). Addison-Wesley Professional. ISBN 978-0321658395.
