# Architecture Complete du Systeme — StreamMG

**Document :** Architecture logicielle detaillee, diagrammes et flux de donnees  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 2.0 (avec role Fournisseur de Contenu)  
**Date :** Fevrier 2026

---

## 1. Vue d'ensemble de l'architecture

StreamMG adopte une architecture client-serveur a trois couches clairement separees. Cette separation, connue sous le nom d'architecture trois-tiers (Three-Tier Architecture), est le choix de reference pour les applications web modernes et constitue un choix academiquement solide et defendable. Comprendre pourquoi cette architecture est adoptee est aussi important que de la decrire : elle garantit que le frontend ne connait pas l'existence de la base de donnees, que la base de donnees ne connait pas l'existence des clients, et que toute la logique metier est centralisee dans le backend, ce qui simplifie la maintenance, les tests, et l'evolution future du systeme.

```
+===============================================================+
|                     COUCHE PRESENTATION                       |
|                                                               |
|  [Client Web - Chrome/Firefox]   [Client Mobile - Expo Go]   |
|  Progressive Web App             iOS / Android                |
|  React Native Web                React Native                 |
|  expo-router, expo-av            expo-router, expo-av         |
|  zustand, TanStack Query         zustand, TanStack Query      |
+========================|======================================+
                         |
                    HTTPS / REST JSON
                    (Authorization: Bearer JWT)
                         |
+========================|======================================+
|                     COUCHE APPLICATIVE                        |
|                                                               |
|              [Serveur Node.js v20 + Express.js v4]           |
|                                                               |
|   /api/auth        /api/contents    /api/history              |
|   /api/admin       /api/provider    /api/payment              |
|                                                               |
|   Middlewares : auth.mw, admin.mw, provider.mw,              |
|                 upload.mw, rateLimiter, helmet, cors          |
|                                                               |
|          Stripe SDK (mode test) --- Stripe API                |
+========|====================|=================================+
         |                    |
         |                    |
+========|========+  +========|========================+
|  COUCHE DONNEES |  |  STOCKAGE FICHIERS MEDIAS       |
|                 |  |                                 |
| [MongoDB v7.x]  |  | [Systeme de fichiers /uploads]  |
|  mongoose v8.x  |  |  /uploads/video/               |
|                 |  |  /uploads/audio/               |
|  users          |  |  /uploads/thumbnails/          |
|  contents       |  |  /uploads/subtitles/           |
|  watchHistory   |  |                                 |
|  playlists      |  +=================================+
|  refreshTokens  |
|  transactions   |
+=================+
```

---

## 2. Architecture frontend : Expo et React Native Web

### 2.1 Le principe du code partage

Le concept central du frontend de StreamMG est d'ecrire un seul code source qui produit simultanement une application web (Progressive Web App dans le navigateur) et une application mobile native (iOS et Android via Expo Go). Ce n'est pas de la magie — c'est une consequence directe du fonctionnement de React Native Web.

React Native repose sur des composants abstraits comme `View`, `Text`, `Image` ou `ScrollView` qui ne correspondent pas directement a des elements HTML. React Native Web est une librairie qui ajoute un "traducteur" : lorsque le code tourne dans un navigateur, `View` devient un `<div>`, `Text` devient un `<span>`, `Image` devient un `<img>`. Lorsque le meme code tourne sur iOS ou Android, ces composants se traduisent en vues natives. Le developpeur (Membre 1) ecrit donc ses composants une seule fois, et la plateforme cible decide comment les rendre.

Expo est l'outil qui orchestre tout cela. Il fournit un bundler unifie, une gestion des assets (images, polices, fichiers audio de demonstration), et des modules qui s'adaptent automatiquement a la plateforme. La commande `npx expo start` lance en meme temps un serveur de developpement pour le web (accessible dans le navigateur) et un serveur pour mobile (accessible via l'application Expo Go scannee par QR code).

### 2.2 Structure de la navigation avec expo-router

expo-router apporte un systeme de navigation base sur le systeme de fichiers, similaire au fonctionnement de Next.js pour le web. Chaque fichier dans le repertoire `app/` correspond a un ecran de l'application. Cette convention elimine la necessite de configurer manuellement un navigateur et rend la structure de l'application immediatement lisible par quelqu'un qui consulte l'arborescence des fichiers.

```
app/
|-- _layout.tsx                  -- Layout racine : Provider zustand, MiniPlayer global
|-- index.tsx                    -- Page d'accueil
|-- (auth)/
|   |-- _layout.tsx              -- Layout pour ecrans non authentifies
|   |-- login.tsx                -- Connexion
|   `-- register.tsx             -- Inscription
|-- (tabs)/
|   |-- _layout.tsx              -- Navigation par onglets (Accueil, Explorer, Profil)
|   |-- index.tsx                -- Accueil : contenu mis en avant, tendances
|   |-- explore.tsx              -- Catalogue complet avec filtres
|   |-- search.tsx               -- Recherche textuelle
|   `-- profile.tsx              -- Profil, historique, gestion du cache hors-ligne
|-- content/
|   `-- [id].tsx                 -- Page de detail d'un contenu (route dynamique)
|-- player/
|   |-- video.tsx                -- Lecteur video plein ecran
|   `-- audio.tsx                -- File d'ecoute et gestion playlist
|-- admin/
|   |-- _layout.tsx              -- Layout admin (verifie role admin)
|   |-- index.tsx                -- Tableau de bord admin
|   |-- upload.tsx               -- Upload d'un contenu
|   |-- contents.tsx             -- Gestion du catalogue complet
|   `-- stats.tsx                -- Statistiques d'utilisation
|-- provider/
|   |-- _layout.tsx              -- Layout fournisseur (verifie role provider)
|   |-- index.tsx                -- Tableau de bord fournisseur
|   |-- upload.tsx               -- Upload de ses propres contenus
|   `-- my-contents.tsx          -- Liste et gestion de ses contenus
`-- payment/
    |-- subscribe.tsx            -- Selection du plan et paiement Stripe
    `-- success.tsx              -- Confirmation de souscription
```

### 2.3 Gestion de l'etat global avec zustand

Deux stores zustand sont definis au niveau racine de l'application.

Le `authStore` contient le profil de l'utilisateur connecte (identifiant, nom, email, role, statut premium), le JWT en memoire vive (pas dans localStorage pour eviter les attaques XSS), et les actions de connexion et de deconnexion. Ce store est initialise au demarrage de l'application par une tentative de renouvellement silencieux du JWT via le refresh token en cookie.

Le `playerStore` contient l'etat complet du lecteur audio : le contenu en cours de lecture, la position en secondes, l'etat de lecture (en lecture, en pause, en chargement, en erreur), la playlist courante et l'index du titre actif dans cette playlist. Ce store alimente le composant `MiniPlayer` place dans le layout racine, ce qui lui garantit une presence persistante quelle que soit la page affichee.

---

## 3. Architecture backend : Node.js et Express.js

### 3.1 Structure modulaire du backend

Le backend est organise selon le principe de separation des responsabilites. Chaque couche a un role unique et defini : les routes declarent les URLs, les controllers contiennent la logique metier, les middlewares gerent les preoccupations transversales, et les models representent les donnees.

```
backend/src/
|-- routes/
|   |-- auth.routes.js           -- POST /register, /login, /refresh, /logout
|   |-- content.routes.js        -- GET /contents, /contents/:id, /featured, /trending
|   |-- history.routes.js        -- GET/POST/DELETE /history
|   |-- admin.routes.js          -- Routes reservees au role admin
|   |-- provider.routes.js       -- Routes reservees au role provider
|   `-- payment.routes.js        -- POST /create-intent, /webhook, GET /status
|
|-- controllers/                 -- Logique metier de chaque domaine
|-- middleware/
|   |-- auth.middleware.js       -- Verification JWT, injection userId dans req
|   |-- admin.middleware.js      -- Verification role === "admin"
|   |-- provider.middleware.js   -- Verification role === "provider" ou "admin"
|   |-- upload.middleware.js     -- Configuration Multer (types, tailles)
|   |-- rateLimiter.middleware.js-- express-rate-limit configure par route
|   `-- errorHandler.middleware.js -- Gestionnaire global d'erreurs
|
|-- models/                      -- Schemas Mongoose (voir document conception BDD)
|-- services/
|   |-- stripe.service.js        -- Logique Stripe isolee (createIntent, webhook)
|   `-- metadata.service.js      -- Extraction metadonnees audio (music-metadata)
|
`-- app.js                       -- Configuration Express, montage des routes
```

### 3.2 Flux de traitement d'une requete type

Pour comprendre comment ces couches interagissent, prenons l'exemple d'une requete de lecture d'un contenu : GET /api/contents/65f3a2b4c8e9d1234567890a.

La requete arrive sur le serveur Nginx, qui la transmet au processus Node.js. Express.js la route vers le middleware d'authentification `auth.middleware.js`, qui extrait le JWT du header `Authorization: Bearer ...`, le verifie avec `jsonwebtoken.verify()`, et injecte l'identifiant et le role de l'utilisateur dans l'objet `req`. La requete continue vers le controller `content.controller.js`, qui appelle `Content.findById(req.params.id)` via Mongoose, incremente le `viewCount` avec `$inc` pour eviter les problemes de concurrence, et retourne le document JSON au frontend. En cas d'erreur (contenu introuvable, base de donnees indisponible), le middleware `errorHandler` capture l'exception et retourne une reponse d'erreur structuree avec le bon code HTTP.

---

## 4. Acteurs du systeme et leurs flux

### 4.1 L'utilisateur standard (role : "user")

L'utilisateur standard s'inscrit, se connecte, navigue dans le catalogue, lit les contenus gratuits, cree des playlists personnelles, et active le mode hors-ligne pour certains titres audio. Il est limite a 5 lectures par jour. Il peut upgrader vers le plan Premium via le flux de paiement Stripe en mode test.

### 4.2 L'utilisateur premium (role : "premium")

L'utilisateur premium dispose de tous les droits de l'utilisateur standard, sans limite de lectures par jour et avec acces aux contenus marques `isPremiumOnly: true`. Son statut est verifie dans le JWT (role "premium") et en base de donnees (champ `isPremium: true` avec `premiumExpiry` dans le futur). Si `premiumExpiry` est depassee, une tache automatique (ou une verification a la connexion) repasse son role a "user".

### 4.3 Le fournisseur de contenu (role : "provider")

Le Fournisseur de Contenu est un nouvel acteur integre dans la version 2.0 de StreamMG. Il represente un producteur ou un detenteur de droits culturels malgaches (un label de musique, un realisateur, une association culturelle) qui dispose d'un compte propre pour deposer ses contenus sur la plateforme, sans avoir acces au tableau de bord administrateur complet.

Les specificites du role provider sont les suivantes. Un provider peut uniquement voir et modifier les contenus qu'il a lui-meme uploades (`uploadedBy === req.userId`). Il ne peut pas voir ni modifier les contenus des autres providers ou de l'admin. Il peut publier ou depublier ses propres contenus (`isPublished`). Il ne peut pas modifier les roles des utilisateurs, consulter les statistiques globales, ni acceder aux informations des autres comptes.

Le middleware `provider.middleware.js` verifie que le role de l'utilisateur est "provider" ou "admin" (l'admin a tous les droits du provider plus les siens). Pour les routes d'edition et de suppression de contenus, un deuxieme niveau de verification dans le controller s'assure que `content.uploadedBy.toString() === req.userId`, garantissant qu'un provider ne peut jamais modifier les contenus d'un autre.

### 4.4 L'administrateur (role : "admin")

L'administrateur dispose d'un acces complet a toutes les fonctionnalites de la plateforme. Il peut gerer tous les contenus (indifferemment de qui les a uploades), consulter les statistiques globales d'utilisation, activer ou desactiver des comptes utilisateurs, et approuver les contenus soumis par les providers avant leur publication.

```
Hierarchie des droits :
admin > provider > premium > user
```

---

## 5. Flux de la simulation de paiement Stripe

Le flux de paiement simule est l'un des aspects techniques les plus importants a comprendre et a maitriser pour la soutenance. Voici le deroulement complet, etape par etape, entre le frontend (Membre 1), le backend (Membre 2) et l'API Stripe externe.

```
[Frontend]                    [Backend Node.js]            [API Stripe - mode test]
    |                               |                               |
    | 1. POST /api/payment/         |                               |
    |    create-intent              |                               |
    |    { plan: "monthly" }        |                               |
    |------------------------------>|                               |
    |                               | 2. stripe.paymentIntents.    |
    |                               |    create({ amount: 500000,  |
    |                               |    currency: "mga" })         |
    |                               |----------------------------->>|
    |                               |                               |
    |                               |<< 3. { id: "pi_...",         |
    |                               |    client_secret: "pi_...    |
    |                               |    _secret_..." }             |
    |                               |                               |
    | 4. { clientSecret:            |                               |
    |    "pi_..._secret_..." }      |                               |
    |<------------------------------|                               |
    |                               |                               |
    | 5. Afficher Stripe Elements   |                               |
    |    Saisie carte :             |                               |
    |    4242 4242 4242 4242        |                               |
    |                               |                               |
    | 6. stripe.confirmCardPayment( |                               |
    |    clientSecret, { card })    |                               |
    |------------------------------------------------------------->>|
    |                               |                               |
    |<<------------------------------------------------------------7|
    |    { paymentIntent:           |                               |
    |      { status: "succeeded" }} |                               |
    |                               |                               |
    |                               |<< 8. Webhook POST /api/      |
    |                               |    payment/webhook           |
    |                               |    Event: payment_intent.    |
    |                               |    succeeded                 |
    |                               |                               |
    |                               | 9. Verifier signature webhook|
    |                               |    Mettre a jour users:      |
    |                               |    isPremium = true          |
    |                               |    role = "premium"          |
    |                               |    premiumExpiry = +30 jours |
    |                               |    Creer transaction doc     |
    |                               |                               |
    | 10. Afficher ecran de         |                               |
    |     confirmation              |                               |
```

L'etape 9 est critique : la mise a jour du statut premium de l'utilisateur doit se faire via le webhook Stripe, pas via la reponse cote client. Cela garantit que meme si le client perd sa connexion apres le paiement, le statut sera mis a jour lorsque le backend recevra le webhook.

---

## 6. Flux du mode hors-ligne (PWA)

Le mode hors-ligne est gere entierement cote client, par le Service Worker. Voici comment le Service Worker intercepte les requetes pour servir les fichiers audio depuis le cache.

```
[Application Web]      [Service Worker]      [Serveur Backend]
    |                        |                      |
    | 1. fetch("/uploads/    |                      |
    |    audio/mora_mora.mp3")|                     |
    |----------------------->|                      |
    |                        | 2. La requete est-   |
    |                        |    elle dans le cache|
    |                        |    "streamMG-offline"|
    |                        |    -audio-v1" ?      |
    |                        |                      |
    |   [Si OUI - hors-ligne possible]              |
    |                        | 3. Retourner la      |
    |                        |    reponse en cache  |
    |<-----------------------|                      |
    |                        |                      |
    |   [Si NON - connexion necessaire]             |
    |                        | 4. Faire la requete  |
    |                        |    au serveur        |
    |                        |--------------------->|
    |                        |<---------------------|
    |                        | 5. Mettre en cache   |
    |                        |    si demande par    |
    |                        |    l'utilisateur     |
    |<-----------------------|                      |
```

---

## 7. Configuration Nginx pour le deploiement

```nginx
# /etc/nginx/sites-available/streamMG

server {
    listen 80;
    server_name api.streamMG.mg;
    return 301 https://$host$request_uri;  # Redirection HTTP -> HTTPS
}

server {
    listen 443 ssl;
    server_name api.streamMG.mg;

    ssl_certificate     /etc/letsencrypt/live/api.streamMG.mg/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.streamMG.mg/privkey.pem;

    # En-tetes de securite (responsabilite Membre 3)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options    "nosniff" always;
    add_header X-Frame-Options           "DENY" always;
    add_header X-XSS-Protection          "1; mode=block" always;

    # Servir les fichiers medias directement (evite de passer par Node.js)
    location /uploads/ {
        alias /var/www/streamMG/uploads/;
        # Restriction : seules les requetes avec un JWT valide peuvent acceder
        # aux fichiers premium (a implementer via auth_request ou validation JWT)
    }

    # Reverse proxy vers Node.js pour les routes API
    location /api/ {
        proxy_pass         http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection 'upgrade';
        proxy_set_header   Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 8. References bibliographiques

Tilkov, S., & Vinoski, S. (2010). Node.js: Using JavaScript to Build High-Performance Network Programs. *IEEE Internet Computing*, 14(6), 80-83. https://doi.org/10.1109/MIC.2010.145

Meta Open Source. (2025). *React Native Web*. https://necolas.github.io/react-native-web

Expo. (2025). *Expo Router v3 — File-based routing*. https://docs.expo.dev/router/introduction

Mozilla Developer Network. (2025). *Service Worker API*. https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API

Nginx. (2025). *Nginx as a Reverse Proxy*. https://nginx.org/en/docs/http/ngx_http_proxy_module.html

Stripe Inc. (2026). *Stripe Webhooks — Listen for events*. https://stripe.com/docs/webhooks

OWASP Foundation. (2023). *Security Headers Reference*. https://owasp.org/www-project-secure-headers

Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall. ISBN 978-0134494166.
