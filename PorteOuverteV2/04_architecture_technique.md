# Architecture Technique — StreamMG

**Document :** Description de l'architecture logicielle et des choix techniques  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 1.0  
**Date :** Fevrier 2026

---

## 1. Vue d'ensemble de l'architecture

StreamMG adopte une architecture client-serveur classique a trois couches, eprouvee et facilement defendable en soutenance academique. La separation claire entre le frontend, le backend et la couche donnees garantit la maintenabilite, la testabilite et la scalabilite future du systeme.

```
+---------------------------+     +---------------------------+
|   CLIENT WEB (Expo Web)   |     |  CLIENT MOBILE (Expo Go)  |
|   Progressive Web App     |     |  iOS / Android            |
+-------------+-------------+     +-------------+-------------+
              |                                 |
              +----------------+----------------+
                               |
                    [ HTTPS - REST JSON ]
                               |
              +----------------+----------------+
              |                                 |
+-------------+-------------+                  |
|    API REST Node.js        |                  |
|    Express.js v4.x         |                  |
|    Port 3000 (dev)         |                  |
|    Reverse proxy Nginx     |                  |
+------+----------+----------+                  |
       |          |          |                  |
  [MongoDB]  [/uploads]  [Stripe API]           |
  v7.x       fichiers    mode test              |
             medias                             |
+-------------------------------------------+  |
|     NGINX — Reverse Proxy + Static Files  +--+
|     Let's Encrypt SSL                     |
+-------------------------------------------+
```

---

## 2. Couche presentation : Expo et React Native Web

### 2.1 Principe du code partage

La decision la plus importante de l'architecture frontend est d'utiliser un unique code source pour produire simultanement l'application web et l'application mobile. Ce principe est rendu possible par React Native Web, une librairie qui traduit les primitives React Native (View, Text, Image, ScrollView, TouchableOpacity) en leurs equivalents HTML (div, span, img, div avec overflow:scroll, button) lors du rendu dans un navigateur web.

Expo sert de couche d'unification au-dessus de React Native et React Native Web. Il fournit un toolchain unifie (Metro Bundler pour le JavaScript, webpack configure par Expo pour le web), une gestion centralisee des assets (images, polices), et un acces harmonise aux API natives des appareils (permissions, stockage, capteurs) via ses propres modules (expo-camera, expo-file-system, etc.). L'instruction `npx expo start` lance simultanement les serveurs de developpement pour toutes les plateformes cibles.

### 2.2 Structure des fichiers du frontend

L'organisation du code frontend suit la convention de expo-router, qui utilise le systeme de fichiers comme definition de la navigation. Chaque fichier dans le repertoire `app/` correspond a un ecran ou a une route de l'application.

```
project-root/
├── app/
│   ├── (auth)/
│   │   ├── login.tsx
│   │   └── register.tsx
│   ├── (tabs)/
│   │   ├── _layout.tsx          -- Navigation par onglets
│   │   ├── index.tsx            -- Page d'accueil
│   │   ├── explore.tsx          -- Catalogue complet
│   │   ├── search.tsx           -- Recherche
│   │   └── profile.tsx          -- Profil utilisateur
│   ├── content/
│   │   └── [id].tsx             -- Page de detail d'un contenu
│   ├── admin/
│   │   ├── _layout.tsx          -- Layout admin protege
│   │   ├── index.tsx            -- Tableau de bord
│   │   ├── upload.tsx           -- Formulaire d'upload
│   │   └── stats.tsx            -- Statistiques
│   ├── payment/
│   │   └── subscribe.tsx        -- Flux abonnement Stripe
│   └── _layout.tsx              -- Layout racine
├── components/
│   ├── VideoPlayer.tsx          -- Lecteur video (expo-av)
│   ├── AudioPlayer.tsx          -- Lecteur audio (expo-av)
│   ├── MiniPlayer.tsx           -- Mini-player persistant
│   ├── ContentCard.tsx          -- Carte de contenu dans le catalogue
│   └── StripePaymentForm.tsx    -- Formulaire Stripe Elements
├── stores/
│   ├── authStore.ts             -- Etat d'authentification (zustand)
│   └── playerStore.ts           -- Etat du lecteur audio (zustand)
├── services/
│   └── api.ts                   -- Client axios configure
└── hooks/
    └── useContents.ts           -- Hooks TanStack Query
```

### 2.3 Gestion de l'etat global

L'etat global de l'application est gere par **zustand**, une librairie minimaliste qui evite la complexite de Redux. Deux stores sont definis.

Le `authStore` contient l'utilisateur connecte (objet avec id, username, email, role, isPremium), le JWT en memoire (non dans localStorage pour des raisons de securite), et les actions de connexion et de deconnexion. Le JWT est stocke en memoire JavaScript (variable du store) et non dans le localStorage ou le sessionStorage, ce qui le protege contre les attaques XSS. Le renouvellement automatique du JWT (via le refresh token en cookie httpOnly) est gere par un intercepteur axios.

Le `playerStore` contient le contenu audio en cours de lecture (objet contenu complet), l'etat de lecture (en cours, pause, chargement), la position de lecture en secondes, et les actions de lecture, pause, et navigation dans la playlist.

### 2.4 Requetes API et mise en cache

Les requetes vers l'API backend sont gerees par **TanStack Query** (anciennement React Query). Cette librairie apporte plusieurs avantages concrets : la mise en cache automatique des reponses API (evite de refaire la meme requete si les donnees sont recentes), la gestion des etats de chargement et d'erreur, la revalidation automatique des donnees au focus de la fenetre ou au retour de l'utilisateur sur l'ecran, et la pagination infinie pour le catalogue.

Le client **axios** est configure avec un intercepteur de requete qui ajoute automatiquement le header `Authorization: Bearer <jwt>` a chaque requete protegee, et un intercepteur de reponse qui detecte les erreurs 401 (JWT expire) et declenche automatiquement un appel a POST /api/auth/refresh pour renouveler le JWT avant de rejouer la requete initiale.

### 2.5 Lecteur audio et video

La librairie **expo-av** est utilisee pour la lecture audio et video sur toutes les plateformes. Elle expose une API JavaScript unifiee qui s'appuie sur les lecteurs natifs de chaque plateforme : AVPlayer sur iOS, ExoPlayer sur Android, et l'element HTML5 `<video>` ou `<audio>` sur le web.

Le composant `AudioPlayer` charge le fichier audio via une URI (URL complete du fichier sur le serveur), configure les options de lecture (loop, volume initial), et expose les controles a l'interface. La position de lecture est lue toutes les 500 millisecondes via le callback `onPlaybackStatusUpdate` d'expo-av, et enregistree en base de donnees toutes les 10 secondes.

Le mini-player est rendu via un composant flottant (`position: 'absolute', bottom: 0`) dans le layout racine de l'application, ce qui le rend persistent lors des navigations entre ecrans.

---

## 3. Couche applicative : API REST Node.js / Express.js

### 3.1 Structure du backend

```
backend/
├── src/
│   ├── routes/
│   │   ├── auth.routes.js
│   │   ├── content.routes.js
│   │   ├── history.routes.js
│   │   ├── admin.routes.js
│   │   └── payment.routes.js
│   ├── controllers/
│   │   ├── auth.controller.js
│   │   ├── content.controller.js
│   │   ├── history.controller.js
│   │   ├── admin.controller.js
│   │   └── payment.controller.js
│   ├── middleware/
│   │   ├── auth.middleware.js    -- Verification JWT
│   │   ├── admin.middleware.js   -- Verification role admin
│   │   └── upload.middleware.js  -- Configuration Multer
│   ├── models/
│   │   ├── User.model.js
│   │   ├── Content.model.js
│   │   ├── WatchHistory.model.js
│   │   ├── Playlist.model.js
│   │   └── RefreshToken.model.js
│   ├── services/
│   │   ├── stripe.service.js
│   │   └── metadata.service.js  -- Extraction metadonnees audio
│   └── app.js
├── uploads/
│   ├── video/
│   ├── audio/
│   └── thumbnails/
├── .env
└── server.js
```

### 3.2 Middleware d'authentification

Le middleware `auth.middleware.js` est applique a toutes les routes necessitant une authentification. Il extrait le JWT de l'en-tete `Authorization: Bearer <token>`, le verifie avec `jsonwebtoken.verify()` en utilisant la cle secrete stockee dans les variables d'environnement, et injecte le payload decode (userId, role) dans l'objet `req` pour que les controllers puissent l'utiliser. Si le JWT est absent ou invalide, il retourne une reponse 401 Unauthorized.

### 3.3 Gestion de l'upload et extraction des metadonnees

Le middleware Multer est configure pour accepter les fichiers audio (audio/mpeg, audio/aac) et video (video/mp4) avec des limites de taille distinctes. Apres le stockage du fichier sur le disque, le controller admin passe le chemin du fichier a la fonction `parseFile()` de la librairie `music-metadata`. Cette fonction lit les metadonnees ID3 embarquees dans le fichier audio et retourne un objet contenant le titre, l'artiste, l'album, la duree en secondes, et la pochette d'album sous forme de buffer binaire. La pochette est convertie en base64 et stockee dans le document MongoDB du contenu, ou enregistree comme fichier image separe dans `/uploads/thumbnails/` selon la taille.

### 3.4 Integration Stripe en mode test

Le fichier `stripe.service.js` encapsule toutes les interactions avec l'API Stripe. La fonction `createPaymentIntent(amount, currency, userId)` cree un PaymentIntent Stripe avec les metadonnees de l'utilisateur, et retourne le `client_secret` au controller. Le controller le transmet au frontend via la reponse HTTP.

La route POST /api/payment/webhook recoit les evenements Stripe. En developpement, la CLI Stripe (commande `stripe listen --forward-to localhost:3000/api/payment/webhook`) intercepte les evenements Stripe de test et les transmet au backend local. En production simulee (pour la soutenance), un endpoint webhook reel est configure dans le tableau de bord Stripe test. La signature de chaque evenement est verifiee avec `stripe.webhooks.constructEvent()` pour s'assurer que l'evenement provient bien de Stripe. L'evenement `payment_intent.succeeded` declenche la mise a jour du statut Premium de l'utilisateur.

---

## 4. Couche donnees : MongoDB et Mongoose

### 4.1 Schemas Mongoose

Le schema `User` definit les champs avec leurs types, validations et valeurs par defaut. Les champs email et username ont la contrainte `unique: true`. Le champ role est un enum valant soit "user" soit "admin". Les timestamps (createdAt, updatedAt) sont actives automatiquement via l'option `{ timestamps: true }`.

Le schema `Content` inclut un champ `type` (enum : "video" ou "audio") qui permet de filtrer facilement les contenus par nature. Les champs specifiques aux audios (artist, album, coverArt) sont optionnels pour ne pas contraindre les documents video. Le champ `viewCount` est incremente via une operation atomique MongoDB `$inc` a chaque lecture, evitant les problemes de concurrence.

Le schema `WatchHistory` utilise une combinaison unique sur les champs `userId` et `contentId` (index compose unique) pour s'assurer qu'un seul document d'historique existe par paire utilisateur/contenu. La mise a jour de la progression utilise `findOneAndUpdate()` avec l'option `upsert: true`, qui cree le document s'il n'existe pas ou le met a jour s'il existe, en une seule operation atomique.

### 4.2 Indexation

Les index MongoDB suivants sont crees pour optimiser les performances des requetes les plus frequentes. Un index texte composite sur les champs `title` et `artist` de la collection `contents` supporte les recherches textuelles. Un index simple sur le champ `category` supporte les filtres par categorie. Un index compose sur `userId` et `lastWatchedAt` dans la collection `watchHistory` supporte les requetes de l'historique utilisateur triees par date. Un index sur `viewCount` decroissant supporte les requetes de tendances (contenus les plus vus).

---

## 5. Securite de l'application

### 5.1 Authentification et gestion des tokens

Le schema de securite repose sur deux tokens complementaires. Le JWT (Access Token) a une duree de vie courte de 15 minutes. Il est signe avec une cle secrete HS256 de 256 bits minimum stockee dans les variables d'environnement. Il contient uniquement le strict necessaire : l'identifiant de l'utilisateur et son role. Il est stocke en memoire JavaScript cote frontend (pas dans localStorage) pour le proteger contre les attaques XSS.

Le Refresh Token a une duree de vie de 7 jours. Il est un token opaque (chaine aleatoire) stocke en base de donnees sous forme hachee (bcrypt). Il est transmis au client dans un cookie httpOnly, Secure, SameSite=Strict, ce qui le protege contre les attaques XSS et CSRF. Lors de chaque utilisation du refresh token pour renouveler un JWT, l'ancien refresh token est invalide et un nouveau est emis (rotation des refresh tokens), ce qui limite la fenetre d'exploitation en cas de vol.

### 5.2 Validation des entrees

Toutes les donnees recues par l'API sont validees avant traitement. Les schemas de validation sont definis avec la librairie `express-validator` ou directement via les schemas Mongoose. Les champs requis, les types, les longueurs minimales et maximales, et les formats (email, URL) sont verifies. Les erreurs de validation retournent une reponse 400 Bad Request avec une liste des erreurs detaillees, sans exposer d'information sensible sur la structure interne du systeme.

---

## 6. Infrastructure de deploiement pour la soutenance

Le backend est deploye sur Railway (platform-as-a-service) avec les variables d'environnement injectees via l'interface Railway (MONGODB_URI, JWT_SECRET, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET). Le frontend web est exporte avec `npx expo export --platform web` et deploye sur Vercel avec une configuration de rewrite pour gerer le routage cote client. La base de donnees MongoDB est hebergee sur MongoDB Atlas (cluster M0 gratuit suffisant pour la demonstration). Les fichiers medias de demonstration sont stockes directement sur Railway (volume persistent configure).

Nginx est configure sur le serveur Railway (ou en local pour la demonstration hors-ligne) comme reverse proxy avec les en-tetes de securite HTTP suivants : Strict-Transport-Security, X-Content-Type-Options: nosniff, X-Frame-Options: DENY, et Content-Security-Policy.

---

## 7. References bibliographiques

Tilkov, S., & Vinoski, S. (2010). Node.js: Using JavaScript to Build High-Performance Network Programs. *IEEE Internet Computing*, 14(6), 80-83. https://doi.org/10.1109/MIC.2010.145

Chodorow, K. (2019). *MongoDB: The Definitive Guide* (3e ed.). O'Reilly Media. ISBN 978-1491954461.

Vieira, M. (2023). *Full-Stack React, TypeScript, and Node*. Packt Publishing. ISBN 978-1839219931.

OWASP Foundation. (2023). *JSON Web Token Cheat Sheet for Java*. https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html

Meta Open Source. (2025). *React Native Web*. https://necolas.github.io/react-native-web

Expo. (2025). *Expo Router — File-based routing for React Native*. https://docs.expo.dev/router/introduction

TanStack. (2025). *TanStack Query v5 — Documentation*. https://tanstack.com/query/latest

Stripe Inc. (2026). *Stripe API Reference — PaymentIntents*. https://stripe.com/docs/api/payment_intents

MongoDB Inc. (2025). *MongoDB Atlas Documentation*. https://www.mongodb.com/docs/atlas

Railway. (2025). *Railway Documentation — Deployments*. https://docs.railway.app
