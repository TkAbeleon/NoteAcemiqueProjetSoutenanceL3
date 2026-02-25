# Cahier des Charges — StreamMG

**Document :** Cahier des Charges Fonctionnel et Technique  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 1.0  
**Date :** Février 2026  
**Redige par :** Membre 3 — Chef de Projet Fonctionnel  
**Valide par :** L'equipe StreamMG

---

## 1. Presentation generale du projet

### 1.1 Identification du projet

StreamMG est une plateforme de streaming audiovisuel cross-platform (web et mobile) dediee a la diffusion et a la decouverte de contenus culturels malgaches. L'application permet aux utilisateurs de visionner des films, series et documentaires, d'ecouter de la musique traditionnelle et moderne malgache, et de consulter des podcasts et emissions culturelles, depuis un navigateur web ou depuis une application mobile iOS et Android.

Le projet est realise dans le cadre de la Licence 3 Genie Logiciel. Il constitue un projet de groupe secondaire, mene en parallele des memoires de licence individuels de chaque membre de l'equipe. Le perimetre est volontairement delimite pour garantir la livraison d'un prototype fonctionnel et demontrable en soutenance.

### 1.2 Contexte et besoin

Le besoin a l'origine du projet est double. D'un cote, les createurs et producteurs de contenus culturels malgaches disposent de peu de canaux de diffusion numerique structures et accessibles localement. De l'autre, les utilisateurs finaux malgaches n'ont pas acces a une plateforme de streaming centralisant les contenus de leur culture, adaptee a leurs contraintes de connectivite et a leur pouvoir d'achat.

StreamMG repond a ce besoin par une solution pragmatique : un MVP (Minimum Viable Product) academique qui pose les bases techniques et fonctionnelles d'une telle plateforme, sans pretendre a une mise en production immediate ou a une concurrence directe avec les acteurs etablis.

### 1.3 Parties prenantes

L'equipe de developpement est composee du Membre 1 (developpeur full-stack, dominante backend), du Membre 2 (ingenieur donnees et tests), et du Membre 3 (chef de projet fonctionnel et redacteur). Le jury academique est la partie prenante principale pour la validation du projet. Les utilisateurs finaux types (etudiants, jeunes adultes malgaches) constituent la cible fonctionnelle pour la conception de l'experience utilisateur.

---

## 2. Description fonctionnelle

### 2.1 Acteurs du systeme

Le systeme distingue trois types d'acteurs.

L'**utilisateur non authentifie** est un visiteur qui accede a la page d'accueil de la plateforme. Il peut consulter le catalogue en mode apercu (titres et visuels visibles, lecture bloquee), effectuer une recherche basique, et acceder aux pages d'inscription et de connexion.

L'**utilisateur authentifie** est un membre inscrit et connecte. Il peut lire les contenus video et audio en streaming, gerer son profil et son historique, creer des playlists personnelles, acceder au mode hors-ligne pour les contenus audio, et souscrire a un abonnement simule via le flux Stripe en mode test.

L'**administrateur** est un utilisateur avec des droits eleves. Il accede a un tableau de bord dedie pour gerer le catalogue (upload, modification, suppression de contenus), consulter les statistiques d'utilisation, et gerer les comptes utilisateurs.

### 2.2 Catalogue de contenus

L'application organise ses contenus selon la hierarchie suivante. Les contenus sont regroupes par type principal (video ou audio), puis par genre ou categorie culturelle. Pour les contenus video, les categories sont : films malgaches, series televisees, documentaires (nature, societe, histoire), emissions culturelles filmees. Pour les contenus audio, les categories sont : hira gasy, salegy, tsapiky, beko, afrobeats malgasy, musique contemporaine, podcasts culturels.

Chaque contenu dispose des attributs minimaux suivants : titre, description, annee de production, categorie principale, sous-categorie optionnelle, langue (malgache, francais, ou billingue), duree, vignette (image de couverture), fichier media (URL du fichier sur le serveur ou lien de streaming), compteur de vues ou d'ecoutes, et date d'ajout dans le systeme.

Pour les contenus audio uniquement, les attributs supplementaires sont : artiste ou groupe, album d'appartenance, et pochette d'album (extraite automatiquement des metadonnees ID3 lors de l'upload).

### 2.3 Fonctionnalites par module

#### Module Authentification

L'inscription requiert un nom d'utilisateur unique, une adresse email valide, et un mot de passe d'au moins 8 caracteres comportant au moins une majuscule et un chiffre. Le mot de passe est hache avec bcrypt (facteur de cout 12) avant stockage en base de donnees. La connexion genere un JWT avec une duree de validite de 15 minutes et un refresh token d'une duree de 7 jours stocke en cookie httpOnly. La deconnexion invalide le refresh token en base de donnees.

#### Module Catalogue

La page d'accueil presente une selection de contenus mis en avant (bandeau hero), les categories disponibles, les contenus les plus regardes ou ecoutes de la semaine, et les ajouts recents. La recherche est textuelle, porte sur les titres et les artistes, et retourne des resultats tries par pertinence. Le filtrage par categorie et par type (video ou audio) est disponible.

#### Module Lecture

Le lecteur video propose les controles standards : lecture/pause, avance/retour de 10 secondes, controle du volume, mode plein ecran, et affichage de la progression. Le lecteur audio propose les controles suivants : lecture/pause, controle du volume, barre de progression interactive, mode repetition (une chanson ou toute la playlist), et mode aleatoire. Le mini-player audio reste visible en bas de l'ecran lors de la navigation entre les pages ou ecrans de l'application, ce qui constitue un point de confort utilisateur essentiel pour une experience d'ecoute continue.

L'historique de lecture enregistre la position de lecture (en secondes) pour chaque contenu et chaque utilisateur. Lorsqu'un utilisateur reprend un contenu, la lecture repart automatiquement a la position enregistree.

#### Module Hors-ligne (Web uniquement)

L'utilisateur peut selectionner des titres audio pour une ecoute hors-ligne. Le Service Worker met en cache les fichiers audio selectionnes dans l'API Cache du navigateur. L'interface indique clairement les titres disponibles hors-ligne avec un indicateur visuel. Le cache expire automatiquement apres 48 heures depuis le moment de la mise en cache. L'utilisateur peut supprimer manuellement des titres du cache hors-ligne.

#### Module Abonnement et Paiement Simule

La plateforme propose deux plans tarifaires fictifs : un plan Gratuit avec acces limite (5 contenus par jour, qualite standard) et un plan Premium avec acces illimite et qualite superieure. Le flux de souscription au plan Premium suit les etapes suivantes.

L'utilisateur clique sur "Passer a Premium". Il est redirige vers la page de selection de plan. Il selectionne la periodicite (mensuelle ou annuelle fictive). Il saisit ses informations de carte via le formulaire Stripe Elements (iframe securise, donnees jamais envoyees directement au backend StreamMG). Il confirme le paiement. Le backend StreamMG cree un PaymentIntent Stripe en mode test et retourne le client_secret. Le frontend confirme le paiement avec Stripe.js en utilisant le client_secret. Stripe retourne le statut de confirmation. Le backend recoit la confirmation via webhook Stripe (simule avec stripe listen en developpement) et met a jour le statut Premium de l'utilisateur en base de donnees. L'utilisateur recoit une notification de confirmation a l'ecran.

Les numeros de carte de test utilises pour les demonstrations sont ceux fournis officiellement par Stripe dans sa documentation : 4242 4242 4242 4242 pour un succes, 4000 0000 0000 9995 pour un echec.

#### Module Administration

Le tableau de bord administrateur est accessible depuis une route protegee (/admin) apres verification du role admin en base de donnees. Il propose les fonctionnalites suivantes : formulaire d'upload de contenus (fichier media, vignette, metadonnees manuelles), liste des contenus avec options de modification et de suppression, statistiques d'utilisation (nombre de lectures par contenu sur les 7 et 30 derniers jours, nombre d'utilisateurs inscrits, nombre d'utilisateurs actifs), et gestion basique des comptes utilisateurs (desactivation d'un compte).

---

## 3. Description technique

### 3.1 Architecture generale

Le systeme adopte une architecture client-serveur a trois couches. La couche presentation est portee par l'application Expo/React Native Web, deployee comme Progressive Web App sur navigateur et comme application mobile via Expo Go. La couche applicative est portee par l'API REST Node.js/Express, qui centralise toutes les regles metier et la securite. La couche donnees est composee de MongoDB pour les donnees structurees et du systeme de fichiers local (repertoire /uploads) pour les fichiers medias.

### 3.2 Stack technologique detaillee

**Frontend :** Expo SDK 52, React Native 0.76.x, React Native Web, expo-router v3.x, expo-av v14.x, zustand v4.x, TanStack Query v5.x, axios, nativewind v4.x, @stripe/stripe-react-native, @stripe/react-stripe-js.

**Backend :** Node.js v20 LTS, Express.js v4.x, jsonwebtoken v9.x, bcryptjs v2.x, multer v1.x, music-metadata v10.x, fluent-ffmpeg, cors, express-rate-limit, dotenv, stripe v14.x, mongoose v8.x.

**Base de donnees :** MongoDB v7.x, Mongoose v8.x.

**Infrastructure :** Nginx (reverse proxy), Let's Encrypt (SSL), Railway ou Render (hebergement backend), Vercel ou Netlify (hebergement frontend web), MongoDB Atlas (base de donnees cloud pour la demo).

**Outils de developpement :** Git, GitHub, Postman, Figma, Trello ou Notion, nodemon, stripe CLI (pour les webhooks en local).

### 3.3 Modele de donnees

Le modele de donnees comprend les collections MongoDB suivantes.

La collection **users** contient les champs : _id (ObjectId), username (String, unique), email (String, unique), passwordHash (String), role (String, enum : user ou admin, defaut : user), isPremium (Boolean, defaut : false), premiumExpiry (Date, optionnel), createdAt (Date), updatedAt (Date).

La collection **contents** contient les champs : _id (ObjectId), title (String), description (String), type (String, enum : video ou audio), category (String), subCategory (String, optionnel), language (String), duration (Number, en secondes), thumbnail (String, URL), filePath (String, chemin serveur), artist (String, optionnel, pour les audios), album (String, optionnel, pour les audios), coverArt (String, URL de la pochette, optionnel), viewCount (Number, defaut : 0), createdAt (Date), updatedAt (Date).

La collection **watchHistory** contient les champs : _id (ObjectId), userId (ObjectId, reference users), contentId (ObjectId, reference contents), progressSeconds (Number), lastWatchedAt (Date).

La collection **playlists** contient les champs : _id (ObjectId), userId (ObjectId, reference users), name (String), contentIds (Array d'ObjectId), createdAt (Date).

La collection **refreshTokens** contient les champs : _id (ObjectId), userId (ObjectId), token (String, hache), expiresAt (Date).

### 3.4 API REST — Principaux endpoints

Les routes d'authentification sont : POST /api/auth/register (inscription), POST /api/auth/login (connexion, retourne JWT et refresh token), POST /api/auth/refresh (renouvellement du JWT via refresh token), POST /api/auth/logout (deconnexion et invalidation du refresh token).

Les routes de catalogue sont : GET /api/contents (liste paginee avec filtres category, type, search), GET /api/contents/:id (detail d'un contenu), GET /api/contents/featured (contenus mis en avant), GET /api/contents/trending (contenus les plus vus/ecoutes).

Les routes de lecture et d'historique sont : POST /api/history/:contentId (enregistrement ou mise a jour de la progression), GET /api/history (historique de l'utilisateur connecte), DELETE /api/history/:contentId (suppression d'une entree).

Les routes d'administration sont protegees par le middleware requireAdmin et comprennent : POST /api/admin/contents (upload d'un contenu), PUT /api/admin/contents/:id (modification), DELETE /api/admin/contents/:id (suppression), GET /api/admin/stats (statistiques d'utilisation).

Les routes de paiement simule sont : POST /api/payment/create-intent (creation d'un PaymentIntent Stripe), POST /api/payment/webhook (reception des evenements Stripe), GET /api/payment/status (statut de l'abonnement de l'utilisateur connecte).

### 3.5 Securite

Le hachage des mots de passe est assure par bcrypt avec un facteur de cout de 12. L'authentification repose sur des JWT a courte duree de vie (15 minutes) associes a des refresh tokens rotatifs stockes en cookie httpOnly pour prevenir les attaques XSS. Le rate limiting est configure a 100 requetes par IP par fenetre de 15 minutes sur les routes d'authentification, et a 200 requetes par IP par fenetre de 15 minutes sur les autres routes. Les en-tetes de securite HTTP sont configures via le middleware helmet. Le CORS est configure pour n'autoriser que les origines declarees (domaine de l'application web et localhost en developpement). Les uploads de fichiers sont valides cote serveur : type MIME verifie (video/mp4, audio/mpeg, audio/aac, image/jpeg, image/png), taille maximale de 500 Mo pour les videos et de 50 Mo pour les audios. Les routes d'administration sont protegees par un middleware de verification du role admin extrait du JWT.

---

## 4. Contraintes et exigences non fonctionnelles

### 4.1 Performance

Le temps de reponse de l'API pour les requetes de liste et de detail doit etre inferieur a 500 ms en conditions normales. Le temps de demarrage du lecteur video ou audio doit etre inferieur a 3 secondes sur une connexion 4G. La pagination de la liste des contenus est limitee a 20 elements par page.

### 4.2 Compatibilite

L'application web doit etre compatible avec les dernières versions de Chrome, Firefox, Safari et Edge. L'application mobile doit fonctionner sur iOS 14+ et Android 10+. La version web doit etre responsive et lisible sur des ecrans a partir de 360 pixels de largeur.

### 4.3 Disponibilite

Pour la demonstration de soutenance, une disponibilite de 99 % sur la duree de la presentation est exigee. Pour la periode de developpement, aucune contrainte de disponibilite n'est imposee.

### 4.4 Accessibilite

Les elements interactifs (boutons, liens, champs de formulaire) doivent etre accessibles au clavier. Les images doivent disposer d'attributs alt descriptifs. Le contraste des couleurs doit respecter les recommandations WCAG 2.1 niveau AA.

---

## 5. Livrables attendus

Les livrables du projet sont les suivants : le code source complet versionne sur GitHub, le prototype fonctionnel deployable (backend sur Railway ou Render, frontend web sur Vercel), l'application mobile demonstrable via Expo Go sur smartphone physique ou emulateur, la documentation technique de l'API (collection Postman exportee), les maquettes Figma (web et mobile), le cahier des charges (present document), le rapport de tests fonctionnels, et le memoire de licence accompagnant le projet.

---

## 6. Planning previsionnel simplifie

La phase de conception, qui comprend la finalisation des maquettes Figma, la conception du schema de donnees et la definition des endpoints API, est prevue sur deux semaines. La phase de developpement du backend (API REST, authentification, upload, streaming, integration Stripe) est prevue sur quatre semaines. La phase de developpement du frontend (navigation, catalogue, lecteurs, formulaires, admin) est prevue en parallele sur quatre semaines. La phase de tests et de correction des anomalies est prevue sur deux semaines. La phase de preparation de la soutenance (memoire, slides, repetition) est prevue sur une semaine.

---

## 7. References bibliographiques

Stripe Inc. (2026). *Stripe Developer Documentation — PaymentIntents API*. https://stripe.com/docs/api/payment_intents

Expo. (2025). *Expo AV — Audio and Video*. https://docs.expo.dev/versions/latest/sdk/av

Mozilla Developer Network. (2025). *Service Worker API*. https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API

OWASP Foundation. (2023). *OWASP Top Ten 2023*. https://owasp.org/www-project-top-ten/

Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures* (These de doctorat). University of California, Irvine.

Mongoose. (2025). *Mongoose v8.x Documentation*. https://mongoosejs.com/docs

Pressman, R. S., & Maxim, B. R. (2019). *Software Engineering: A Practitioner's Approach* (9e ed.). McGraw-Hill Education. ISBN 978-1259872976.
