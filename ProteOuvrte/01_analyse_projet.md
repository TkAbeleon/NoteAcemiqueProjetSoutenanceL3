# Analyse du Projet — StreamMG

**Titre :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Niveau :** Licence 3 Génie Logiciel  
**Type :** Projet de groupe secondaire, obligatoire  
**Equipe :** 3 membres  
**Date :** Février 2026

---

## 1. Contexte et problématique

Madagascar possède un patrimoine audiovisuel et musical d'une grande richesse : le hira gasy, le salegy, le tsapiky, le beko, sans compter les documentaires sur la biodiversite unique de l'ile, les productions cinematographiques locales et les emissions culturelles radiophoniques. Ce patrimoine reste pourtant absent, ou presque, des grandes plateformes internationales de diffusion numerique. Netflix, Spotify, Amazon Prime Video ou YouTube Premium proposent des catalogues massivement orientes vers les productions occidentales. Les rares contenus africains ou malgaches qui y figurent ne representent qu'une fraction marginale de l'offre disponible, inaccessible de surcroit pour une majorite de la population en raison du cout des abonnements.

Ce vide culturel numerique constitue le point de depart du present projet. Il ne s'agit pas de concurrencer ces plateformes dans leur modele economique ou leur infrastructure technique, mais de demontrer, dans un cadre academique de niveau Licence, qu'il est possible de concevoir une solution de diffusion audiovisuelle adaptee aux contraintes locales et centree sur la valorisation du contenu malgache.

Le contexte numerique de Madagascar presente des caracteristiques structurelles qu'il convient de comprendre precisement avant toute decision d'architecture. Selon DataReportal (2025), le pays compte environ 18,2 millions de connexions mobiles actives, soit 56,2 % de la population totale. En revanche, le taux de penetration d'internet au sens large ne depasse pas 20,4 %, avec 6,6 millions d'internautes declares. Cette asymetrie est fondamentale : le mobile est le premier et souvent le seul terminal numerique accessible pour la population malgache. Une plateforme accessible uniquement depuis un navigateur de bureau serait structurellement inadaptee a ce marche.

La bande passante disponible est par ailleurs tres inegale selon les regions. Dans les zones urbaines comme Antananarivo, Toamasina ou Mahajanga, une connexion 4G est generalement accessible mais reste couteuse relativement au pouvoir d'achat local. Dans les zones periurbaines et rurales, la 3G, voire la 2G, dominent encore largement. Toute plateforme de streaming destinee a ce contexte doit integrer des mecanismes d'adaptation au debit disponible, une compression raisonnee des medias, et une capacite de consultation partielle hors connexion.

La problematique academique du projet se formule ainsi : comment concevoir et implementer, dans les contraintes d'un projet de Licence avec une equipe de trois membres disposant chacun d'un memoire individuel principal, une plateforme de diffusion audiovisuelle adaptee aux contraintes d'infrastructure numerique malgaches, valorisant le patrimoine culturel local, et demontrant la maitrise d'une architecture logicielle full-stack moderne ?

---

## 2. Objectifs du projet

### 2.1 Objectif principal

L'objectif principal est de developper une application cross-platform accessible simultanement sur navigateur web et sur mobile iOS et Android, permettant la diffusion en streaming de contenus video et audio malgaches, avec gestion des utilisateurs, catalogue organise par genres culturels, et consultation partielle hors connexion.

### 2.2 Objectifs secondaires

Le projet vise a offrir une navigation fluide dans un catalogue structure par categories et genres culturels malgaches. Il cherche a proposer une experience de lecture continue avec reprise automatique de la progression. Il doit maintenir une coherence d'experience utilisateur entre les versions web et mobile, issues d'une meme base de code. Il doit integrer un espace d'administration fonctionnel permettant la gestion du catalogue et le suivi de statistiques elementaires. Il doit enfin proposer une simulation de paiement, sans traitement financier reel, afin d'illustrer le flux d'abonnement dans une perspective d'evolution produit.

### 2.3 Objectifs academiques

Sur le plan academique, le projet vise a demontrer la capacite de l'equipe a concevoir une architecture logicielle complete et coherente, a appliquer les principes du developpement full-stack, a mettre en oeuvre une demarche de gestion de projet rigoureuse, et a produire une documentation technique suffisamment structuree pour etre defendue en soutenance.

---

## 3. Perimetre fonctionnel

### 3.1 Fonctionnalites incluses dans le MVP

Le MVP (Minimum Viable Product) constitue le perimetre de livraison cible pour la soutenance.

**Catalogue et navigation.** L'application propose un catalogue organise en categories distinctes : films, series, documentaires, musique traditionnelle (hira gasy, salegy, tsapiky, beko), podcasts et emissions culturelles. La navigation par categorie et la recherche textuelle par titre ou par artiste sont incluses.

**Streaming video.** La lecture video en ligne est assuree via le composant expo-av de React Native. Les formats supportes sont MP4 (codec H.264) pour mobile et web.

**Streaming audio.** La lecture audio est integree dans la meme application, avec extraction automatique des metadonnees ID3 lors de l'upload (titre, artiste, duree, pochette d'album via la librairie music-metadata cote Node.js). Les formats supportes sont MP3 et AAC. Un lecteur audio persistant (mini-player) reste visible lors de la navigation entre les ecrans.

**Gestion des utilisateurs.** L'inscription et la connexion sont securisees par JWT avec refresh token. Chaque utilisateur dispose d'un profil personnel, d'un historique de visionnage et d'ecoute, et d'une section "Continuer a regarder/ecouter".

**Mode hors-ligne partiel.** Sur la version web, le Service Worker permet la mise en cache temporaire de contenus audio selectionnes, pour une ecoute sans connexion active. Le cache expire automatiquement apres 48 heures.

**Recommandation simple.** Le systeme de recommandation est fonde sur la popularite (nombre d'ecoutes et de vues) et sur les categories les plus consultees par l'utilisateur connecte. Aucun algorithme de machine learning n'est implique.

**Espace administrateur.** Un tableau de bord permet l'upload et la gestion des contenus, ainsi que la consultation de statistiques elementaires : contenus les plus vus et ecoutes, nombre d'utilisateurs actifs sur les 7 derniers jours.

**Simulation de paiement.** Un flux d'abonnement simule est integre via Stripe en mode test. L'utilisateur peut selectionner un plan tarifaire, saisir des informations de carte factices fournies par Stripe, et recevoir une confirmation d'activation simulee. Aucune transaction financiere reelle n'est effectuee.

### 3.2 Fonctionnalites explicitement exclues

Les elements suivants sont hors perimetre : le traitement de paiement en production, le streaming live, la recommandation par intelligence artificielle, la protection DRM avancee, le transcodage automatique a grande echelle, et la publication sur les stores applicatifs.

---

## 4. Analyse des choix technologiques

### 4.1 Frontend : Expo et React Native Web

La decision architecturale la plus structurante du projet est l'adoption d'Expo SDK 52 avec React Native Web comme unique base de code frontend. Ce choix permet de produire simultanement une application mobile native via Expo Go et une Progressive Web App, a partir d'un code source partage a plus de 80 %.

React Native Web, maintenu par Meta, traduit les composants React Native en elements HTML/CSS lors du rendu sur navigateur. Expo unifie le toolchain (bundler Metro, gestion des assets, acces aux API natives) et facilite le deploiement multi-plateforme. La librairie expo-av gere de maniere unifiee la lecture audio et video sur toutes les plateformes cibles.

Les librairies frontend utilisees sont les suivantes :

- expo-av (v14.x) : lecture audio et video unifiee sur toutes les plateformes
- expo-router (v3.x) : navigation basee sur le systeme de fichiers, compatible web et mobile
- react-query / TanStack Query (v5.x) : gestion du cache des requetes API et de l'etat asynchrone
- axios : requetes HTTP vers l'API backend
- @stripe/stripe-react-native : formulaire de paiement simule sur mobile
- @stripe/stripe-js et @stripe/react-stripe-js : formulaire de paiement simule sur web
- zustand (v4.x) : gestion de l'etat global (utilisateur connecte, etat du mini-player audio)
- nativewind (v4.x) : styling via une syntaxe Tailwind CSS adaptee a React Native

### 4.2 Backend : Node.js et Express.js

Node.js v20 LTS associe a Express.js v4.x constitue le socle du serveur d'application. Ce choix est aligne avec les competences du Membre 1 et avec l'ecosysteme JavaScript partage avec le frontend. Le backend expose une API RESTful consommee par le frontend. Les echanges de donnees sont en JSON. L'authentification repose sur les JWT transmis dans les en-tetes HTTP Authorization.

Les librairies backend utilisees sont les suivantes :

- jsonwebtoken (v9.x) : generation et verification des JWT
- bcryptjs (v2.x) : hachage securise des mots de passe, facteur de cout 12
- multer (v1.x) : gestion de l'upload de fichiers video, audio et images
- music-metadata (v10.x) : extraction des metadonnees ID3 des fichiers audio
- fluent-ffmpeg avec ffmpeg-static : verification et conversion optionnelle des formats medias
- cors : gestion des politiques Cross-Origin Resource Sharing
- express-rate-limit : limitation a 100 requetes par IP par fenetre de 15 minutes sur les routes sensibles
- dotenv : gestion des variables d'environnement
- stripe (v14.x) : SDK officiel Stripe pour la simulation de paiement en mode test
- mongoose (v8.x) : ODM entre Node.js et MongoDB

### 4.3 Base de donnees : MongoDB et Mongoose

MongoDB v7.x est retenu comme systeme de gestion de base de donnees. La nature semi-structuree des metadonnees des contenus audiovisuels justifie ce choix : un film possede des attributs differents d'un titre musical, et un schema relationnel rigide introduirait une complexite de modelisation non justifiee. MongoDB stocke les donnees sous forme de documents BSON flexibles. Mongoose est utilise pour definir des schemas de validation et des modeles JavaScript types.

### 4.4 Simulation de paiement avec Stripe en mode test

La simulation de paiement est implementee via le SDK Stripe en mode test. Stripe propose un environnement de test complet, techniquement identique a la production, mais sans aucune transaction financiere reelle. En mode test, Stripe fournit des numeros de carte factices documentes : 4242 4242 4242 4242 pour simuler un paiement reussi, 4000 0000 0000 9995 pour simuler un refus de carte, et 4000 0025 0000 3155 pour declencher une authentification 3D Secure.

Le frontend utilise les composants Stripe Elements, c'est-a-dire un formulaire de saisie de carte integre via iframe securise. Le backend cree un PaymentIntent via l'API Stripe avec le montant et la devise, retourne le client_secret au frontend, et le frontend confirme le paiement cote client. Le backend recoit ensuite la confirmation via un webhook Stripe simule localement avec la commande stripe listen durant le developpement.

### 4.5 Infrastructure et deploiement

En developpement, l'application tourne localement avec npx expo start pour le frontend et nodemon pour le backend. Pour la demonstration de soutenance, le backend est deploye sur un VPS ou sur Railway (tier gratuit), avec Nginx configure comme reverse proxy et un certificat SSL Let's Encrypt. La version web Expo est exportee en mode statique via npx expo export --platform web et hebergee sur Vercel ou Netlify.

---

## 5. Architecture globale du systeme

L'architecture adoptee est une architecture client-serveur a trois couches : la couche presentation (frontend Expo/React Native Web), la couche applicative (API REST Node.js/Express), et la couche donnees (MongoDB et systeme de fichiers local).

```
[Client Web Navigateur]      [Application Mobile Expo Go]
           \                          /
            \                        /
             [  HTTPS / REST JSON  ]
                        |
         [ Serveur Node.js / Express.js ]
                    /          \
                   /            \
           [MongoDB]     [Stockage /uploads]
                                 |
                      [Stripe API - mode test]
```

La communication entre le client et le serveur est entierement asynchrone et repose sur des requetes HTTPS. Le frontend ne communique jamais directement avec la base de donnees. Toutes les operations de lecture et d'ecriture transitent par l'API backend, qui joue le role de gardien des regles metier et de la securite.

---

## 6. Analyse des risques

**Risque 1 — Surcharge du Membre 1.** Le Membre 1 porte la majeure partie du developpement technique. Son memoire individuel principal partage partiellement le meme ecosysteme technologique, ce qui attenue ce risque, mais un derapage de planning reste possible. La mitigation consiste a definir un perimetre strict du MVP et a prioriser les fonctionnalites bloquantes des le debut du projet.

**Risque 2 — Compatibilite React Native Web.** Certains composants React Native ne s'affichent pas parfaitement sur navigateur web. La mitigation consiste a utiliser systematiquement les composants de base (View, Text, ScrollView, TouchableOpacity) et a tester les deux plateformes a chaque etape de developpement.

**Risque 3 — Performance du streaming video sur connexions lentes.** La mitigation consiste a proposer plusieurs niveaux de qualite video en encodant les contenus de demonstration en 360p, 480p et 720p, et a limiter la taille des fichiers utilises pour la soutenance.

**Risque 4 — Volume des fichiers medias.** Les fichiers video peuvent saturer rapidement le stockage serveur. La mitigation consiste a limiter la taille des uploads en developpement et a documenter clairement la solution de stockage cloud envisagee pour la production.

**Risque 5 — Delais lies aux trois memoires principaux.** La mitigation consiste a planifier les jalons du projet streaming en tenant compte des deadlines connues des memoires individuels de chaque membre.

---

## 7. Repartition des roles

**Membre 1 — Developpeur Full-Stack** : architecture globale, API REST Node.js/Express, authentification JWT, upload Multer, extraction metadonnees audio, streaming, integration Stripe, frontend Expo/React Native Web. Memoire principal : plateforme collaborative de gestion d'idees innovantes.

**Membre 2 — Ingenieur Donnees et Tests** : conception du schema MongoDB, modeles Mongoose, indexation, optimisation des requetes, tests fonctionnels Postman, validation des donnees. Memoire principal : systeme de diagnostic medical assiste.

**Membre 3 — Chef de Projet Fonctionnel** : analyse des besoins, maquettes Figma, cahier des charges, redaction du memoire, coordination, preparation soutenance. Memoire principal : plateforme IA de suivi des feux de brousse et de la deforestation a Madagascar (donnees NASA MODIS/VIIRS, IA classique et generative).

---

## 8. References bibliographiques

DataReportal. (2025). *Digital 2025 : Madagascar — Global Digital Insights*. Kepios Analysis. https://datareportal.com/reports/digital-2025-madagascar

GSMA Intelligence. (2025). *The Mobile Economy Sub-Saharan Africa 2025*. GSM Association. https://www.gsma.com/mobileeconomy

Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional. ISBN 978-0321127426.

Chodorow, K. (2019). *MongoDB: The Definitive Guide* (3e ed.). O'Reilly Media. ISBN 978-1491954461.

Stripe Inc. (2026). *Stripe Developer Documentation — Testing*. https://stripe.com/docs/testing

Meta Open Source. (2025). *React Native Web — Documentation officielle*. https://necolas.github.io/react-native-web

Expo. (2025). *Expo Documentation — SDK 52*. https://docs.expo.dev

Mozilla Developer Network. (2025). *Progressive Web Apps — Service Worker API*. https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API

OWASP Foundation. (2023). *OWASP Top Ten 2023*. https://owasp.org/www-project-top-ten/

UNESCO. (2023). *Culture numerique et diversite culturelle dans les pays en developpement*. UNESCO Publishing.

Newman, S. (2021). *Building Microservices: Designing Fine-Grained Systems* (2e ed.). O'Reilly Media. ISBN 978-1492034025.
