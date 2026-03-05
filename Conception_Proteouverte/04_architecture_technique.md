# Architecture Technique — StreamMG

**Document :** Architecture logicielle détaillée  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026

---

## 1. Vue d'ensemble

StreamMG adopte le pattern multi-client avec backend partagé. Deux clients frontend distincts et indépendants — une application mobile (React Native/Expo, Membre 1) et une application web (React.js/Vite, Membre 2) — consomment la même API REST Node.js/Express développée par le Membre 3. La base de données MongoDB est commune aux deux clients et gérée entièrement par le backend.

```
+---------------------------+       +------------------------------+
|  APPLICATION MOBILE       |       |  APPLICATION WEB             |
|  React Native + Expo 52   |       |  React.js 18 + Vite 5        |
|  Membre 1                 |       |  Membre 2                    |
|                           |       |                              |
|  expo-av (lecture native) |       |  react-player (HTML5)        |
|  expo-file-system         |       |  Service Worker PWA          |
|  expo-secure-store        |       |  Cookie httpOnly             |
|  @stripe/stripe-rn        |       |  @stripe/react-stripe-js     |
|  NativeWind + zustand     |       |  Tailwind CSS + zustand      |
+-----------+---------------+       +--------------+---------------+
            |                                      |
            +------------------+-------------------+
                               |
              [ HTTPS / REST JSON + JWT ]
                               |
+------------------------------+------------------------------+
|  API REST — Node.js v20 + Express.js v4                   |
|  Membre 3                                                  |
|                                                            |
|  Middleware checkAccess — verification niveau d'acces      |
|  JWT (15min) + Refresh Token (7j) + bcrypt (cout 12)       |
|  Multer upload + music-metadata extraction ID3             |
|  Helmet headers + CORS + Rate limiting + express-validator |
|  Stripe SDK mode test (abonnement + achat unitaire)        |
|                                                            |
|  Routes : auth / contents / history / tutorial            |
|           provider / admin / payment                       |
+-------+---------------------------+------------------------+
        |                           |
+-------+-------+   +---------------+------------------+
|  MongoDB v7   |   |  /uploads                        |
|  users        |   |    /video  /audio  /thumbnails   |
|  contents     |   +----------------------------------+
|  watchHistory |           |
|  playlists    |   [Stripe API — mode test]
|  refreshTokens|
|  transactions |
|  purchases    |   <- acces unitaires permanents
|  tutorialProg.|   <- progression dans les tutoriels
+---------------+
```

L'API est strictement agnostique du client : qu'une requête provienne du smartphone Android d'Antananarivo ou du navigateur Chrome d'un utilisateur web, elle reçoit le même traitement et retourne la même réponse JSON. Cette propriété est le fondement de l'architecture multi-client.

---

## 2. Stack technologique complète

### 2.1 Application mobile — Membre 1

| Composant | Technologie | Rôle |
|---|---|---|
| Framework | React Native 0.76 + Expo SDK 52 | Application native iOS/Android |
| Navigation | expo-router v3 | Navigation fichier (file-based routing) |
| Lecture média | expo-av v14 | Lecteur vidéo et audio natif |
| Mode paysage | expo-screen-orientation | Rotation automatique en lecture vidéo |
| Stockage local | expo-file-system | Téléchargement audio hors-ligne |
| Token sécurisé | expo-secure-store | Refresh token (iOS Keychain / Android Keystore) |
| Paiement | @stripe/stripe-react-native | CardField natif (abonnement + achat) |
| État global | zustand v4 | authStore, playerStore, cartStore |
| Requêtes API | TanStack Query v5 | Cache, invalidation, états de chargement |
| Client HTTP | axios | Intercepteur 401 → renouvellement JWT |
| Styling | NativeWind v4 | Classes Tailwind en React Native |

### 2.2 Application web — Membre 2

| Composant | Technologie | Rôle |
|---|---|---|
| Bibliothèque UI | React.js 18 | Interface utilisateur |
| Build tool | Vite 5 | Bundler, HMR, optimisation |
| Navigation | react-router-dom v6 | SPA routing |
| Lecture média | react-player v2 | Lecteur vidéo/audio HTML5 |
| Mode hors-ligne | Service Worker (Workbox) | Cache First audio, expiration 48h |
| Paiement | @stripe/react-stripe-js | Stripe Elements iframe (abonnement + achat) |
| État global | zustand v4 | Structure identique au mobile |
| Requêtes API | TanStack Query v5 | Cache, invalidation |
| Client HTTP | axios | Intercepteur 401 → renouvellement JWT |
| Styling | Tailwind CSS v3 | Utility-first CSS |
| TypeScript | TypeScript | Typage statique |

### 2.3 Backend — Membre 3

| Composant | Technologie | Rôle |
|---|---|---|
| Environnement | Node.js v20 LTS | Runtime serveur |
| Framework | Express.js v4 | Routage, middleware |
| ODM | Mongoose v8 | Schémas MongoDB, validation |
| Auth tokens | jsonwebtoken v9 | JWT HS256, 15 min |
| Hachage | bcryptjs | Mots de passe (coût 12) + hash refresh tokens |
| Upload | Multer v1 | Fichiers multipart, validation MIME/taille |
| Métadonnées audio | music-metadata v10 | Extraction ID3 automatique |
| Paiement | stripe SDK v14 | PaymentIntent, webhook, mode test |
| Headers sécurité | helmet | HSTS, X-Frame-Options, CSP, X-Content-Type |
| CORS | cors | 2 origines autorisées (web prod + localhost) |
| Rate limiting | express-rate-limit | 10 req/15min auth, 200 req/15min autres |
| Validation | express-validator | Validation et sanitisation des entrées |
| Documentation | Postman | Collection exportée, exemples de réponses |

### 2.4 Infrastructure

| Composant | Solution |
|---|---|
| Base de données | MongoDB Atlas (cluster M0 gratuit) |
| Hébergement backend | Railway |
| Hébergement web | Vercel (SPA avec règle rewrite) |
| Démonstration mobile | Expo Go (QR code → URL API staging) |
| Reverse proxy | Nginx + Let's Encrypt SSL |
| Versioning | Git / GitHub |

---

## 3. Le middleware checkAccess — cœur du modèle économique

Le middleware `checkAccess` est la pièce la plus importante de l'architecture côté sécurité. Il est monté sur toutes les routes de streaming (`GET /api/contents/:id/stream`) et de récupération des leçons (`GET /api/contents/:id/lessons`). Il applique les règles du modèle économique côté serveur, indépendamment de ce qu'affiche le client.

```javascript
// middleware/checkAccess.middleware.js
async function checkAccess(req, res, next) {
  const content = await Content.findById(req.params.id).select('accessType price');
  if (!content) return res.status(404).json({ message: 'Contenu introuvable' });

  switch (content.accessType) {

    case 'free':
      // Accessible a tous, meme les visiteurs non connectes (req.user peut etre null)
      return next();

    case 'premium':
      if (!req.user)
        return res.status(403).json({ reason: 'login_required' });
      if (req.user.role !== 'premium' && req.user.role !== 'admin')
        return res.status(403).json({ reason: 'subscription_required' });
      return next();

    case 'paid':
      if (!req.user)
        return res.status(403).json({ reason: 'login_required' });
      if (req.user.role === 'admin') return next();

      // Verification dans la collection purchases — valable pour Standard ET Premium
      const purchase = await Purchase.findOne({
        userId: req.user.id,
        contentId: content._id
      });
      if (!purchase)
        return res.status(403).json({
          reason: 'purchase_required',
          price: content.price  // Le frontend utilise ce prix pour l'ecran d'achat
        });
      return next();

    default:
      return res.status(403).json({ reason: 'access_denied' });
  }
}
```

Ce middleware est intentionnellement court et lisible. Chaque branche du switch correspond exactement à une règle métier documentée dans le cahier des charges. Toute la logique d'autorisation est encapsulée en un seul endroit — principe de séparation des responsabilités.

---

## 4. Gestion de l'authentification

### 4.1 JWT et refresh token

L'authentification repose sur deux tokens. Le **JWT** (durée 15 min, signé HS256) est transmis dans le header `Authorization: Bearer`. Il est stocké en mémoire vive uniquement (variable zustand) pour éviter les attaques XSS. Le **refresh token** (durée 7 jours) est soumis à rotation systématique : à chaque renouvellement, l'ancien est invalidé en base et un nouveau est émis. Il est stocké de manière sécurisée : cookie httpOnly sur le web, expo-secure-store sur mobile (iOS Keychain / Android Keystore).

Au démarrage de l'application mobile, le authStore vérifie la présence d'un refresh token en SecureStore. Si présent et valide, il appelle POST /api/auth/refresh pour obtenir un nouveau JWT. L'utilisateur est reconnecté silencieusement.

### 4.2 Intercepteur axios

Un intercepteur axios intercepte les réponses 401 sur les deux plateformes. Il tente automatiquement de renouveler le JWT via POST /api/auth/refresh, puis rejoue la requête initiale avec le nouveau token. Si le renouvellement échoue (refresh token expiré ou révoqué), l'utilisateur est déconnecté et redirigé vers la page de connexion.

---

## 5. Différences d'implémentation mobile vs web

| Fonctionnalité | Mobile (Membre 1) | Web (Membre 2) |
|---|---|---|
| **Refresh token stockage** | expo-secure-store (natif chiffré) | Cookie httpOnly (géré navigateur) |
| **Lecture vidéo** | expo-av → AVPlayer (iOS) / ExoPlayer (Android) | react-player → `<video>` HTML5 |
| **Lecture audio** | expo-av unifié | react-player → `<audio>` HTML5 |
| **Mode hors-ligne** | expo-file-system, fichier local | Service Worker, Cache API |
| **Mini-player persistant** | Layout racine expo-router | App.tsx hors RouterProvider |
| **Paiement Stripe** | @stripe/stripe-react-native (CardField natif) | @stripe/react-stripe-js (Elements iframe) |
| **Orientation vidéo** | expo-screen-orientation (paysage auto) | CSS fullscreen API |

Ces différences illustrent comment deux technologies distinctes répondent aux mêmes besoins fonctionnels, en tirant parti des capacités propres à chaque plateforme.

---

## 6. Flux d'achat unitaire

```
[Frontend Mobile ou Web]     [Backend Node.js]        [Stripe API]
         |                          |                       |
1. POST /api/payment/purchase       |                       |
   { contentId }                    |                       |
   --------------------------->     |                       |
                                    | 2. Vérifier doublon   |
                                    |    dans purchases     |
                                    |                       |
   [Si doublon]                     |                       |
   <--- 409 "Déjà acheté"           |                       |
                                    |                       |
   [Si premier achat]               |                       |
                                    | 3. stripe.paymentIntents
                                    |    .create({          |
                                    |      amount: price,   |
                                    |      metadata: {      |
                                    |        type:"purchase"|
                                    |        userId,        |
                                    |        contentId }    |
                                    |    })                 |
                                    | --------------------> |
                                    | <-------------------- |
   <--- { clientSecret }            |                       |
         |                          |                       |
4. Afficher formulaire Stripe       |                       |
5. Saisir 4242 4242 4242 4242       |                       |
6. confirmCardPayment()             |                       |
   -------------------------------------------------->      |
   <--------------------------------------------------      |
7. { status: "succeeded" }          |                       |
                                    |                       |
                                    | <----- 8. Webhook     |
                                    |    payment_intent.    |
                                    |    succeeded          |
                                    |    metadata.type =    |
                                    |    "purchase"         |
                                    |                       |
                                    | 9. Créer document     |
                                    |    purchases          |
                                    |    { userId,          |
                                    |      contentId,       |
                                    |      stripePaymentId, |
                                    |      amount,          |
                                    |      purchasedAt }    |
         |                          |                       |
10. Écran confirmation              |                       |
11. Bouton "Lire" actif             |                       |
```

La distinction par `metadata.type` dans le webhook est essentielle : elle permet au backend de distinguer un événement d'abonnement d'un événement d'achat unitaire et d'appeler la bonne logique.

---

## 7. Configuration CORS

```javascript
const corsOptions = {
  origin: function (origin, callback) {
    const allowedOrigins = [
      'https://streamMG-web.vercel.app',  // Web production
      'http://localhost:5173',             // Vite dev
      'http://localhost:8081',             // Expo web dev
    ];
    // Pas d'origin = requete native (mobile Expo Go, Postman)
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Non autorisé par CORS'));
    }
  },
  credentials: true,  // Necessaire pour les cookies httpOnly (refresh token web)
};
```

---

## 8. Déploiement pour la soutenance

Le backend est déployé sur Railway avec les variables d'environnement : `MONGODB_URI`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`. Nginx est configuré en reverse proxy avec SSL Let's Encrypt. Le frontend web est déployé sur Vercel avec une règle de rewrite dirigeant toutes les routes non reconnues vers `index.html` (nécessaire pour le SPA). Le frontend mobile est démontré via Expo Go avec un QR code pointant vers l'URL de l'API de staging. Les webhooks Stripe sont configurés en CLI Stripe pour le développement local et via le tableau de bord Stripe pour le staging.

---

## 9. Références bibliographiques

Stripe Inc. (2026). *Stripe API Reference — PaymentIntents with metadata*. https://stripe.com/docs/api/payment_intents/object#payment_intent_object-metadata

Stripe Inc. (2026). *Webhooks — Handling events*. https://stripe.com/docs/webhooks

Martin, R. C. (2017). *Clean Architecture*. Prentice Hall. ISBN 978-0134494166.

MongoDB Inc. (2025). *MongoDB — Unique Indexes*. https://www.mongodb.com/docs/manual/core/index-unique

OWASP Foundation. (2023). *OWASP Top Ten 2023*. https://owasp.org/www-project-top-ten/

Expo. (2025). *expo-secure-store Documentation*. https://docs.expo.dev/versions/latest/sdk/securestore

TanStack. (2025). *TanStack Query v5*. https://tanstack.com/query/latest

Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures* (Thèse de doctorat). University of California, Irvine.
