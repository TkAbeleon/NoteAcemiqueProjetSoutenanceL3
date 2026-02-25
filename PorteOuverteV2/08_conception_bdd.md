# Conception de la Base de Donnees — StreamMG

**Document :** Modelisation et schema de la base de donnees  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 1.0  
**Date :** Fevrier 2026  
**Responsable :** Membre 2 — Developpeur Backend

---

## 1. Choix du systeme de gestion de base de donnees

StreamMG utilise MongoDB (v7.x), un systeme de gestion de base de donnees oriente documents (NoSQL). Ce choix repond a plusieurs contraintes specifiques du projet.

La premiere contrainte est la nature heterogene des donnees de contenus. Un film possede des attributs specifiques (resolution, sous-titres disponibles, annee de production) qui different de ceux d'un titre musical (artiste, album, pochette, paroles optionnelles) ou d'un podcast (animateur, episode, transcription). Dans un schema relationnel classique, cela imposerait soit une table unique avec de nombreuses colonnes nulles, soit une hierarchie de tables liees par des jointures complexes. MongoDB resout ce probleme en permettant des documents de structure variable au sein d'une meme collection.

La deuxieme contrainte est la flexibilite des metadonnees. Les contenus culturels malgaches sont tres varies et il est difficile d'anticiper a l'avance tous les champs qui pourraient etre utiles. MongoDB permet d'ajouter des attributs a un document existant sans migration de schema.

La troisieme contrainte est la vitesse de developpement dans le contexte d'un projet academique avec des delais courts. Mongoose, l'ODM (Object Document Mapper) utilise par dessus MongoDB, permet de definir des schemas de validation flexibles en JavaScript, ce qui est coherent avec l'ecosysteme Node.js du backend.

---

## 2. Vue d'ensemble des collections

La base de donnees StreamMG comprend six collections principales. Chaque collection correspond a un agregat logique de donnees et est concue pour minimiser les jointures tout en preservant la coherence des donnees.

```
Base de donnees : streamMG
|
|-- users               (comptes utilisateurs, roles, statut premium)
|-- contents            (catalogue video et audio)
|-- watchHistory        (progression de lecture par utilisateur et par contenu)
|-- playlists           (playlists personnelles des utilisateurs)
|-- refreshTokens       (tokens de renouvellement de session)
|-- transactions        (enregistrement des paiements simules Stripe)
```

---

## 3. Schema detaille de chaque collection

### 3.1 Collection : users

La collection users centralise toutes les informations relatives aux comptes de la plateforme. Elle distingue quatre roles : "user" (utilisateur standard), "premium" (utilisateur ayant souscrit au plan Premium simule), "provider" (fournisseur de contenu avec droits d'upload limites a ses propres contenus), et "admin" (administrateur avec acces complet).

```
users {
  _id          : ObjectId          -- Identifiant unique genere par MongoDB
  username     : String            -- Nom d'utilisateur unique, 3-30 caracteres
  email        : String            -- Adresse email unique, validee par regex
  passwordHash : String            -- Hachage bcrypt du mot de passe (prefixe $2b$)
  role         : String            -- Enum : "user" | "premium" | "provider" | "admin"
  isPremium    : Boolean           -- Acces premium actif (defaut : false)
  premiumExpiry: Date              -- Date d'expiration du premium (null si non premium)
  avatar       : String            -- URL de l'image de profil (optionnel)
  bio          : String            -- Biographie courte (optionnel, pour les providers)
  isActive     : Boolean           -- Compte actif ou desactive par admin (defaut : true)
  createdAt    : Date              -- Date de creation automatique (Mongoose timestamps)
  updatedAt    : Date              -- Date de derniere modification automatique
}

Index :
  email   : unique index
  username: unique index
  role    : index simple (pour les requetes admin filtrant par role)
```

Le champ `role` merite une attention particuliere dans la conception. Un utilisateur peut avoir le role "premium" qui est distinct du simple booleen `isPremium`. Cette duplication apparente est intentionnelle : le role "premium" permet des verifications rapides du type d'acteur via le JWT (qui embarque le role), tandis que `isPremium` et `premiumExpiry` permettent une gestion fine de l'expiration de l'abonnement, independamment du role stocke dans le token (qui peut etre expire).

### 3.2 Collection : contents

La collection contents est le coeur du catalogue. Elle regroupe les contenus video et audio dans une seule collection, differencies par le champ `type`. Les champs communs a tous les types sont definis directement, tandis que les champs specifiques a un type (audio ou video) sont optionnels.

```
contents {
  _id          : ObjectId          -- Identifiant unique
  title        : String            -- Titre du contenu, obligatoire
  description  : String            -- Description longue, obligatoire
  type         : String            -- Enum : "video" | "audio"
  category     : String            -- Categorie principale (ex : "film", "salegy", "podcast")
  subCategory  : String            -- Sous-categorie optionnelle (ex : "traditionnel", "moderne")
  language     : String            -- Enum : "mg" | "fr" | "bilingual"
  duration     : Number            -- Duree en secondes (extrait automatiquement pour l'audio)
  thumbnail    : String            -- URL de la vignette principale
  filePath     : String            -- Chemin du fichier media sur le serveur
  fileSize     : Number            -- Taille du fichier en octets
  mimeType     : String            -- Type MIME du fichier (video/mp4, audio/mpeg, etc.)
  viewCount    : Number            -- Nombre total de lectures (defaut : 0)
  isPublished  : Boolean           -- Contenu visible dans le catalogue (defaut : false)
  isPremiumOnly: Boolean           -- Reserve aux abonnes premium (defaut : false)
  uploadedBy   : ObjectId          -- Reference vers users._id (admin ou provider)

  -- Champs specifiques aux contenus audio (optionnels pour les videos) --
  artist       : String            -- Artiste ou groupe
  album        : String            -- Album d'appartenance
  coverArt     : String            -- URL de la pochette d'album (extraite des ID3)
  trackNumber  : Number            -- Numero de piste dans l'album (optionnel)

  -- Champs specifiques aux contenus video (optionnels pour les audios) --
  resolution   : String            -- Ex : "1080p", "720p", "480p"
  subtitles    : Array of Object   -- [{ language: "fr", filePath: "..." }, ...]
  director     : String            -- Realisateur (optionnel)
  cast         : Array of String   -- Liste des acteurs principaux (optionnel)

  createdAt    : Date
  updatedAt    : Date
}

Index :
  title + artist  : index texte composite (pour la recherche full-text)
  category        : index simple (pour les filtres de catalogue)
  type            : index simple (pour le filtre video/audio)
  viewCount       : index decroissant (pour les requetes "tendances")
  uploadedBy      : index simple (pour les requetes "mes contenus" du provider)
  isPublished     : index simple (pour filtrer les contenus visibles)
```

### 3.3 Collection : watchHistory

La collection watchHistory enregistre la progression de lecture de chaque utilisateur pour chaque contenu. Elle permet la fonctionnalite "Continuer a regarder/ecouter" qui est un element central de l'experience utilisateur de toute plateforme de streaming.

```
watchHistory {
  _id             : ObjectId     -- Identifiant unique
  userId          : ObjectId     -- Reference vers users._id
  contentId       : ObjectId     -- Reference vers contents._id
  progressSeconds : Number       -- Position de lecture en secondes
  isCompleted     : Boolean      -- true si l'utilisateur a atteint la fin (defaut : false)
  lastWatchedAt   : Date         -- Date de derniere mise a jour de la progression
}

Index :
  { userId, contentId } : index compose unique (un seul document par paire utilisateur/contenu)
  { userId, lastWatchedAt } : index compose decroissant (pour la section "Continuer a regarder")
  contentId : index simple (pour les agregations de statistiques par contenu)
```

Le choix d'un index compose unique sur `{userId, contentId}` est fondamental. Il garantit qu'il n'existera jamais qu'un seul document d'historique pour une paire utilisateur/contenu donnee. Les mises a jour de progression utilisent l'operation `findOneAndUpdate` avec l'option `{ upsert: true }`, qui cree le document s'il n'existe pas, ou le met a jour s'il existe, en une seule operation atomique. Cette approche evite les doublons et les problemes de concurrence lors de mises a jour frequentes (toutes les 10 secondes pendant la lecture).

### 3.4 Collection : playlists

La collection playlists permet aux utilisateurs authentifies de creer des listes de lecture personnalisees melant contenus audio et video. Un utilisateur peut posseder plusieurs playlists.

```
playlists {
  _id        : ObjectId          -- Identifiant unique
  userId     : ObjectId          -- Reference vers users._id (proprietaire)
  name       : String            -- Nom de la playlist, obligatoire
  description: String            -- Description courte (optionnel)
  contentIds : Array of ObjectId -- Liste ordonnee de references vers contents._id
  isPublic   : Boolean           -- Playlist visible publiquement (defaut : false)
  createdAt  : Date
  updatedAt  : Date
}

Index :
  userId : index simple (pour retrouver toutes les playlists d'un utilisateur)
```

### 3.5 Collection : refreshTokens

La collection refreshTokens stocke les refresh tokens actifs, qui permettent aux utilisateurs de renouveler leur JWT (access token) sans se reconnecter. Le stockage en base de donnees (plutot qu'en memoire) permet l'invalidation explicite d'un token lors de la deconnexion, meme si le token n'est pas encore expire.

```
refreshTokens {
  _id       : ObjectId   -- Identifiant unique
  userId    : ObjectId   -- Reference vers users._id
  tokenHash : String     -- Hash bcrypt du refresh token (jamais le token en clair)
  expiresAt : Date       -- Date d'expiration (7 jours apres creation)
  createdAt : Date
}

Index :
  tokenHash  : index unique (pour la verification rapide lors du renouvellement)
  expiresAt  : index TTL avec expireAfterSeconds: 0 (MongoDB supprime automatiquement
               les documents expires, nettoyage automatique sans tache cron)
  userId     : index simple (pour la deconnexion de tous les appareils d'un utilisateur)
```

L'index TTL (Time To Live) sur `expiresAt` est une fonctionnalite specifique de MongoDB qui supprime automatiquement les documents dont la valeur du champ indexe est dans le passe. Cela elimine le besoin d'une tache de nettoyage periodique.

### 3.6 Collection : transactions

La collection transactions enregistre chaque tentative de paiement simule, qu'elle ait reussi ou echoue. Elle constitue un historique des abonnements qui peut etre consulte par l'administrateur et, en version reduite, par l'utilisateur dans son profil.

```
transactions {
  _id             : ObjectId   -- Identifiant unique
  userId          : ObjectId   -- Reference vers users._id
  stripePaymentId : String     -- Identifiant du PaymentIntent Stripe (commence par "pi_")
  plan            : String     -- Enum : "premium_monthly" | "premium_yearly"
  amount          : Number     -- Montant en centimes (ex : 500000 pour 5000 Ar)
  currency        : String     -- Code devise (ex : "mga" pour ariary malgache)
  status          : String     -- Enum : "pending" | "succeeded" | "failed" | "canceled"
  stripeEvent     : Object     -- Copie de l'evenement webhook Stripe recu (pour audit)
  createdAt       : Date
  updatedAt       : Date
}

Index :
  userId          : index simple (pour l'historique des paiements d'un utilisateur)
  stripePaymentId : index unique (pour la verification des webhooks, evite le traitement double)
  status          : index simple (pour les statistiques admin)
```

---

## 4. Diagramme de relations entre collections

Bien que MongoDB soit une base de donnees non relationnelle, les relations entre collections existent via des references (ObjectId). Le diagramme suivant illustre ces relations.

```
users (1) ----< watchHistory (N)  [un utilisateur, plusieurs entrees d'historique]
users (1) ----< playlists (N)     [un utilisateur, plusieurs playlists]
users (1) ----< refreshTokens (N) [un utilisateur, plusieurs tokens actifs (multi-appareils)]
users (1) ----< transactions (N)  [un utilisateur, plusieurs tentatives de paiement]
users (1) ----< contents (N)      [un provider/admin peut uploader plusieurs contenus]

contents (1) ----< watchHistory (N) [un contenu, plusieurs entrees d'historique]
contents (N) ----< playlists (N)   [relation N-N : un contenu dans plusieurs playlists,
                                    une playlist contient plusieurs contenus]
```

La relation entre `contents` et `playlists` est de type N-N. Elle est implementee par un tableau d'ObjectId (`contentIds`) stocke directement dans le document playlist, evitant une collection de liaison supplementaire. Ce choix est valide car le nombre de contenus par playlist est limite (moins de 1000 dans le contexte du MVP) et les playlists sont toujours chargees avec leurs contenus dans les requetes applicatives.

---

## 5. Exemple de documents MongoDB

L'exemple suivant illustre deux documents de la collection `contents` pour illustrer la flexibilite du schema : un document de type "video" et un document de type "audio".

### Document video (film malgache)

```json
{
  "_id": "65f3a2b4c8e9d1234567890a",
  "title": "Ambiaty",
  "description": "Un film dramatique malgache racontant l'histoire d'une famille de pecheurs...",
  "type": "video",
  "category": "film",
  "subCategory": "drame",
  "language": "mg",
  "duration": 5820,
  "thumbnail": "/uploads/thumbnails/ambiaty_thumb.jpg",
  "filePath": "/uploads/video/ambiaty_720p.mp4",
  "fileSize": 1258291200,
  "mimeType": "video/mp4",
  "viewCount": 347,
  "isPublished": true,
  "isPremiumOnly": false,
  "uploadedBy": "65f3a1c4c8e9d1234567891b",
  "resolution": "720p",
  "subtitles": [{ "language": "fr", "filePath": "/uploads/subtitles/ambiaty_fr.vtt" }],
  "director": "Razanajatovo Henri",
  "cast": ["Rakotondrabe Solo", "Randriamanantena Voahangy"],
  "createdAt": "2026-01-15T10:30:00.000Z",
  "updatedAt": "2026-02-10T08:15:00.000Z"
}
```

### Document audio (titre musical salegy)

```json
{
  "_id": "65f3a2b4c8e9d1234567890b",
  "title": "Mora Mora",
  "description": "Un titre salegy emblematique du nord de Madagascar...",
  "type": "audio",
  "category": "salegy",
  "subCategory": "traditionnel",
  "language": "mg",
  "duration": 243,
  "thumbnail": "/uploads/thumbnails/mora_mora_cover.jpg",
  "filePath": "/uploads/audio/mora_mora.mp3",
  "fileSize": 9720000,
  "mimeType": "audio/mpeg",
  "viewCount": 1284,
  "isPublished": true,
  "isPremiumOnly": false,
  "uploadedBy": "65f3a1c4c8e9d1234567891c",
  "artist": "Tarika Sammy",
  "album": "Salegy Classics Vol.1",
  "coverArt": "/uploads/thumbnails/salegy_classics_cover.jpg",
  "trackNumber": 3,
  "createdAt": "2026-01-20T14:00:00.000Z",
  "updatedAt": "2026-01-20T14:00:00.000Z"
}
```

---

## 6. Agregations MongoDB pour les fonctionnalites cles

### Recuperer la section "Continuer a regarder" d'un utilisateur

```javascript
// Cette agregation joint watchHistory avec contents pour retourner
// les 10 derniers contenus non termines de l'utilisateur, avec leurs details.
db.watchHistory.aggregate([
  {
    $match: {
      userId: ObjectId("..."),   // ID de l'utilisateur connecte
      isCompleted: false         // Exclure les contenus termines
    }
  },
  { $sort: { lastWatchedAt: -1 } },   // Les plus recents d'abord
  { $limit: 10 },
  {
    $lookup: {
      from: "contents",
      localField: "contentId",
      foreignField: "_id",
      as: "content"
    }
  },
  { $unwind: "$content" },
  {
    $project: {
      progressSeconds: 1,
      lastWatchedAt: 1,
      "content.title": 1,
      "content.thumbnail": 1,
      "content.duration": 1,
      "content.type": 1
    }
  }
])
```

### Recuperer le top 10 des contenus les plus vus (7 derniers jours)

```javascript
// Cette agregation joint watchHistory avec contents pour retourner
// les 10 contenus les plus lus depuis 7 jours, avec leur nombre de lectures.
db.watchHistory.aggregate([
  {
    $match: {
      lastWatchedAt: { $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) }
    }
  },
  {
    $group: {
      _id: "$contentId",
      playCount: { $sum: 1 }
    }
  },
  { $sort: { playCount: -1 } },
  { $limit: 10 },
  {
    $lookup: {
      from: "contents",
      localField: "_id",
      foreignField: "_id",
      as: "content"
    }
  },
  { $unwind: "$content" },
  {
    $project: {
      playCount: 1,
      "content.title": 1,
      "content.thumbnail": 1,
      "content.type": 1,
      "content.category": 1
    }
  }
])
```

---

## 7. References bibliographiques

Chodorow, K. (2019). *MongoDB: The Definitive Guide* (3e ed.). O'Reilly Media. ISBN 978-1491954461.

MongoDB Inc. (2025). *MongoDB v7.x Manual — Data Modeling*. https://www.mongodb.com/docs/manual/core/data-modeling-introduction

MongoDB Inc. (2025). *MongoDB Aggregation Pipeline*. https://www.mongodb.com/docs/manual/core/aggregation-pipeline

Mongoose. (2025). *Mongoose v8.x — Schema Guide*. https://mongoosejs.com/docs/guide.html

Elmasri, R., & Navathe, S. B. (2015). *Fundamentals of Database Systems* (7e ed.). Pearson. ISBN 978-0133970777.
