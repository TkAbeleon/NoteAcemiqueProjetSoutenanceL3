# Conception de la Base de Données — StreamMG

**Document :** Modélisation et schéma de la base de données  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026  
**Responsable :** Membre 3 — Développeur Backend

---

## 1. Choix de MongoDB

StreamMG utilise MongoDB (v7.x) comme système de gestion de base de données. Ce choix est justifié par la nature hétérogène des contenus de la plateforme : un film possède des attributs (résolution, réalisateur, distribution, sous-titres) qui n'ont pas de sens pour un titre audio (artiste, album, numéro de piste, pochette). Un tutoriel possède un tableau de leçons imbriquées qui n'existe ni dans les films ni dans les chants. Le modèle document JSON de MongoDB accueille cette flexibilité naturellement, sans colonnes nullable ni tables de jointure complexes.

L'ajout de nouveaux champs (comme `accessType`, `price`, `isTutorial`, `lessons`) se fait sans migration : les documents existants conservent leur structure, et les nouveaux champs sont simplement absents pour eux. Les valeurs par défaut définies dans Mongoose garantissent la cohérence pour les nouveaux documents.

---

## 2. Vue d'ensemble des huit collections

```
Base de données : streamMG
│
├── users              — Comptes, rôles, statut premium
├── contents           — Catalogue : films, chants, docs, tutoriels
├── watchHistory       — Progression de lecture (position en secondes)
├── playlists          — Listes de lecture personnelles
├── refreshTokens      — Tokens de renouvellement de session (hachés)
├── transactions       — Registre des paiements Stripe (abonnements)
├── purchases          — Achats unitaires permanents (contenus payants)
└── tutorialProgress   — Progression dans les séries de leçons
```

---

## 3. Schémas détaillés

### 3.1 Collection users

```javascript
{
  _id          : ObjectId,
  username     : String,    // Unique, 3–30 caractères
  email        : String,    // Unique, format email validé
  passwordHash : String,    // Hachage bcrypt (préfixe $2b$, coût 12)
  role         : String,    // Enum : "user" | "premium" | "provider" | "admin"
  isPremium    : Boolean,   // Défaut false
  premiumExpiry: Date,      // null si non premium, J+30 ou J+365 selon le plan
  avatar       : String,    // URL optionnelle
  isActive     : Boolean,   // Défaut true — désactivation admin sans suppression
  createdAt    : Date,      // Mongoose timestamps
  updatedAt    : Date,
}

Index :
  email    UNIQUE       — Login et vérification d'unicité à l'inscription
  username UNIQUE       — Vérification d'unicité à l'inscription
  role     simple       — Requêtes admin "liste des fournisseurs"
```

### 3.2 Collection contents

La collection centrale du catalogue. Elle couvre tous les types de contenus grâce à la flexibilité du modèle document.

```javascript
{
  _id          : ObjectId,
  title        : String,    // Obligatoire
  description  : String,    // Obligatoire
  type         : String,    // Enum : "video" | "audio"
  category     : String,    // film, salegy, hira-gasy, tsapiky, documentaire, podcast, tutoriel...
  subCategory  : String,    // Optionnel
  language     : String,    // Enum : "mg" | "fr" | "bilingual"
  thumbnail    : String,    // URL de la vignette
  filePath     : String,    // Chemin du fichier principal (absent si isTutorial: true)
  fileSize     : Number,    // Taille en octets
  mimeType     : String,    // Ex : "video/mp4", "audio/mpeg"
  duration     : Number,    // Durée en secondes (absent si isTutorial: true)
  viewCount    : Number,    // Défaut 0, incrémenté via $inc atomique MongoDB
  isPublished  : Boolean,   // Défaut false — passe à true après validation admin
  uploadedBy   : ObjectId,  // Référence vers users._id

  // Champs audio optionnels (null pour les vidéos)
  artist       : String,
  album        : String,
  coverArt     : String,    // URL de la pochette (extraite via music-metadata ou uploadée)
  trackNumber  : Number,

  // Champs vidéo optionnels (null pour les audios)
  resolution   : String,    // Ex : "720p", "1080p"
  director     : String,
  cast         : [String],
  subtitles    : [{ language: String, filePath: String }],

  // Modèle économique — niveau d'accès
  accessType   : String,    // Enum : "free" | "premium" | "paid" — Défaut "free"
                            // Pilier du modèle économique. Lu par checkAccess
                            // sur chaque tentative de streaming.

  price        : Number,    // Montant en centimes Stripe, null si accessType !== "paid"
                            // Exemple : 800000 = 8 000 Ar
                            // Obligatoire et > 0 si accessType === "paid" (validation Mongoose)

  // Tutoriels
  isTutorial   : Boolean,   // Défaut false
  lessons      : [          // Présent uniquement si isTutorial: true
    {
      order       : Number, // Position dans la série (commence à 1)
      title       : String,
      description : String,
      filePath    : String, // Fichier média de cette leçon
      duration    : Number, // Durée en secondes
    }
  ],

  createdAt    : Date,
  updatedAt    : Date,
}

Index :
  { title, artist }  TEXTE   — Recherche full-text dans le catalogue
  category           simple   — Filtre par catégorie
  type               simple   — Filtre vidéo / audio
  accessType         simple   — Filtre admin par niveau d'accès
  viewCount          desc     — Requêtes "Tendances" (top 10)
  uploadedBy         simple   — Requêtes "Mes contenus" du fournisseur
  isPublished        simple   — Exclusion des contenus non publiés
  isTutorial         simple   — Filtre section Tutoriels du catalogue
```

**Décision de conception — embedding des leçons.** Les leçons sont des sous-documents imbriqués dans le document parent, pas une collection séparée. Cette approche (embedding) est choisie car les leçons n'ont pas d'existence indépendante de leur tutoriel : elles sont toujours chargées avec lui, jamais interrogées seules par d'autres entités. L'embedding évite un $lookup (jointure MongoDB) sur chaque requête de catalogue et simplifie le code.

### 3.3 Collection watchHistory

```javascript
{
  _id             : ObjectId,
  userId          : ObjectId,  // Référence users._id
  contentId       : ObjectId,  // Référence contents._id
  progressSeconds : Number,    // Position de lecture en secondes
  isCompleted     : Boolean,   // Défaut false — true quand ≥ 90 % de la durée atteinte
  lastWatchedAt   : Date,

  // Pour les tutoriels, contentId référence l'ID du tutoriel (pas de la leçon)
  // La progression par leçon est gérée dans tutorialProgress
}

Index :
  { userId, contentId } UNIQUE  — Un seul document par paire utilisateur/contenu
  { userId, lastWatchedAt } desc — Section "Continuer à regarder"
```

### 3.4 Collection playlists

```javascript
{
  _id        : ObjectId,
  userId     : ObjectId,
  name       : String,
  description: String,     // Optionnel
  contentIds : [ObjectId], // Liste ordonnée de références vers contents._id
  isPublic   : Boolean,    // Défaut false
  createdAt  : Date,
  updatedAt  : Date,
}

Index : userId simple
```

### 3.5 Collection refreshTokens

```javascript
{
  _id       : ObjectId,
  userId    : ObjectId,
  tokenHash : String,  // Hash bcrypt du token (jamais le token en clair)
  expiresAt : Date,    // J+7 depuis la création

  // La rotation systématique : à chaque renouvellement de JWT, l'ancien document
  // est supprimé et un nouveau est créé avec un nouveau token et un nouveau hash.
}

Index :
  tokenHash  UNIQUE      — Recherche rapide à la vérification
  expiresAt  TTL (expireAfterSeconds: 0) — Suppression automatique des tokens expirés
  userId     simple      — Invalidation de toutes les sessions d'un utilisateur
```

### 3.6 Collection transactions

Registre complet des paiements Stripe (abonnements). Chaque événement webhook d'abonnement crée ou met à jour un document dans cette collection.

```javascript
{
  _id             : ObjectId,
  userId          : ObjectId,
  stripePaymentId : String,  // Identifiant PaymentIntent ("pi_...")
  plan            : String,  // Enum : "premium_monthly" | "premium_yearly"
  amount          : Number,  // Montant en centimes
  currency        : String,  // "mga" (ariary malgache)
  status          : String,  // Enum : "pending" | "succeeded" | "failed" | "canceled"
  stripeEvent     : Object,  // Copie de l'événement webhook complet — pour audit
  createdAt       : Date,
  updatedAt       : Date,
}

Index :
  userId          simple  — Historique de paiements d'un utilisateur
  stripePaymentId UNIQUE  — Prévient le traitement double d'un même événement
  status          simple  — Statistiques admin par statut
```

### 3.7 Collection purchases — achats unitaires

La collection `purchases` enregistre les achats unitaires confirmés. **La présence d'un document dans cette collection pour une paire (userId, contentId) constitue le titre d'accès permanent à ce contenu.** C'est cette collection que le middleware `checkAccess` interroge pour les contenus de type "paid".

```javascript
{
  _id             : ObjectId,
  userId          : ObjectId,  // Référence users._id
  contentId       : ObjectId,  // Référence contents._id (le contenu acheté)
  stripePaymentId : String,    // Identifiant PaymentIntent Stripe ("pi_...")
                               // Garantit la traçabilité entre l'achat en base
                               // et le paiement Stripe correspondant.
  amount          : Number,    // Montant payé en centimes au moment de l'achat.
                               // Conservé pour l'historique : si le fournisseur
                               // change le prix plus tard, l'historique reste exact.
  purchasedAt     : Date,      // Horodatage de la confirmation par le webhook Stripe.
                               // (Distinct de createdAt qui peut différer)
}

Index :
  { userId, contentId } UNIQUE
    La contrainte d'unicité la plus importante du système.
    Elle garantit l'idempotence : un utilisateur ne peut pas posséder deux fois
    le même contenu. En cas de double-clic ou de retour arrière côté client,
    l'insertion dupliquée échoue silencieusement en base de données,
    et le backend retourne 409 à l'utilisateur.

  stripePaymentId UNIQUE
    Prévient l'insertion double si le webhook Stripe est délivré plusieurs fois
    (ce qui peut arriver en cas de timeout réseau — comportement normal de Stripe).

  userId simple     — Requête "Mes achats" dans le profil
  contentId simple  — Statistiques admin par contenu
```

### 3.8 Collection tutorialProgress — progression dans les tutoriels

Un document dans cette collection est créé lors du premier accès à un tutoriel et mis à jour à chaque leçon consultée ou terminée.

```javascript
{
  _id              : ObjectId,
  userId           : ObjectId,  // Référence users._id
  contentId        : ObjectId,  // Référence contents._id (le tutoriel, isTutorial: true)
  lastLessonIndex  : Number,    // Index (base 0) de la dernière leçon consultée.
                                // Utilisé par le bouton "Continuer" pour reprendre
                                // directement à la bonne leçon.
  completedLessons : [Number],  // Indices des leçons terminées (≥ 90 % de leur durée).
  percentComplete  : Number,    // Calculé : completedLessons.length / lessons.length × 100.
                                // Stocké en base pour éviter de recalculer sur chaque requête.
  startedAt        : Date,      // Date du premier accès au tutoriel.
  lastUpdatedAt    : Date,      // Mise à jour à chaque progression.
}

Index :
  { userId, contentId } UNIQUE
    Un seul document de progression par paire utilisateur/tutoriel.
    L'opération Mongoose utilise findOneAndUpdate avec upsert: true —
    crée le document s'il n'existe pas, le met à jour s'il existe.

  userId simple          — Requête "Mes tutoriels en cours" dans le profil
  lastUpdatedAt desc     — Tri par activité récente dans la section "Continuer"
```

---

## 4. Diagramme de relations

```
users (1) ────< watchHistory (N)
users (1) ────< playlists (N)
users (1) ────< refreshTokens (N)
users (1) ────< transactions (N)
users (1) ────< purchases (N)
users (1) ────< tutorialProgress (N)
users (1) ────< contents (N)          [via uploadedBy — fournisseur]

contents (1) ────< watchHistory (N)
contents (1) ────< purchases (N)
contents (1) ────< tutorialProgress (N)
contents (N) >────< playlists (N)     [relation N-N via tableau contentIds]
```

---

## 5. Exemples de documents JSON

### Tutoriel (collection contents)

```json
{
  "_id": "65f3a2b4c8e9d1234567890c",
  "title": "Apprendre le salegy de Diego-Suarez — 8 leçons",
  "description": "Une série complète pour apprendre les bases du salegy.",
  "type": "video",
  "category": "tutoriel",
  "subCategory": "musique-traditionnelle",
  "language": "mg",
  "thumbnail": "/uploads/thumbnails/tuto_salegy_cover.jpg",
  "viewCount": 412,
  "isPublished": true,
  "uploadedBy": "65f3a1c4c8e9d1234567891c",
  "accessType": "premium",
  "price": null,
  "isTutorial": true,
  "lessons": [
    {
      "order": 1,
      "title": "Introduction : origines du salegy",
      "description": "Histoire et contexte culturel du salegy du nord de Madagascar.",
      "filePath": "/uploads/video/salegy_lecon1.mp4",
      "duration": 480
    },
    {
      "order": 2,
      "title": "Les rythmes de base",
      "description": "Apprendre les patterns rythmiques fondamentaux à la guitare.",
      "filePath": "/uploads/video/salegy_lecon2.mp4",
      "duration": 720
    }
  ],
  "createdAt": "2026-01-20T09:00:00.000Z",
  "updatedAt": "2026-02-01T14:30:00.000Z"
}
```

### Film payant (collection contents)

```json
{
  "_id": "65f3a2b4c8e9d1234567890d",
  "title": "Avant-première : Ny Fitiavana",
  "description": "Film romantique malgache, exclusivité de la plateforme.",
  "type": "video",
  "category": "film",
  "language": "mg",
  "duration": 6240,
  "thumbnail": "/uploads/thumbnails/ny_fitiavana_thumb.jpg",
  "filePath": "/uploads/video/ny_fitiavana_720p.mp4",
  "viewCount": 89,
  "isPublished": true,
  "uploadedBy": "65f3a1c4c8e9d1234567891d",
  "accessType": "paid",
  "price": 800000,
  "isTutorial": false,
  "resolution": "720p",
  "director": "Haja Rakoto"
}
```

### Achat unitaire (collection purchases)

```json
{
  "_id": "65f3a2b4c8e9d1234567890e",
  "userId": "65f3a2b4c8e9d12345678901",
  "contentId": "65f3a2b4c8e9d1234567890d",
  "stripePaymentId": "pi_3OqXkT2eZvKYlo2C1aB2cD3e",
  "amount": 800000,
  "purchasedAt": "2026-02-15T16:22:10.000Z"
}
```

### Progression tutoriel (collection tutorialProgress)

```json
{
  "_id": "65f3a2b4c8e9d1234567890f",
  "userId": "65f3a2b4c8e9d12345678901",
  "contentId": "65f3a2b4c8e9d1234567890c",
  "lastLessonIndex": 1,
  "completedLessons": [0, 1],
  "percentComplete": 25,
  "startedAt": "2026-02-10T20:00:00.000Z",
  "lastUpdatedAt": "2026-02-12T21:30:00.000Z"
}
```

---

## 6. Agrégations MongoDB

### Tutoriels en cours d'un utilisateur

```javascript
db.tutorialProgress.aggregate([
  {
    $match: {
      userId: ObjectId("..."),
      percentComplete: { $lt: 100 }    // Exclure les tutoriels terminés
    }
  },
  { $sort: { lastUpdatedAt: -1 } },    // Plus récemment consultés en premier
  { $limit: 10 },
  {
    $lookup: {
      from: "contents",
      localField: "contentId",
      foreignField: "_id",
      as: "tutorial"
    }
  },
  { $unwind: "$tutorial" },
  {
    $project: {
      percentComplete: 1,
      lastLessonIndex: 1,
      lastUpdatedAt: 1,
      "tutorial.title": 1,
      "tutorial.thumbnail": 1,
      totalLessons: { $size: "$tutorial.lessons" }
    }
  }
])
```

### Statistiques de ventes simulées (admin — 30 derniers jours)

```javascript
db.purchases.aggregate([
  {
    $match: {
      purchasedAt: {
        $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      }
    }
  },
  {
    $group: {
      _id: "$contentId",
      totalSales: { $sum: 1 },
      totalRevenue: { $sum: "$amount" }
    }
  },
  { $sort: { totalRevenue: -1 } },
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
      totalSales: 1,
      totalRevenue: 1,
      "content.title": 1,
      "content.uploadedBy": 1
    }
  }
])
```

---

## 7. Références bibliographiques

Chodorow, K. (2019). *MongoDB: The Definitive Guide* (3e éd.). O'Reilly Media. ISBN 978-1491954461.

MongoDB Inc. (2025). *MongoDB v7.x Manual — Embedded Documents*. https://www.mongodb.com/docs/manual/core/data-modeling-embedded-data

MongoDB Inc. (2025). *MongoDB Aggregation Pipeline*. https://www.mongodb.com/docs/manual/core/aggregation-pipeline

MongoDB Inc. (2025). *MongoDB Indexes*. https://www.mongodb.com/docs/manual/indexes

Mongoose. (2025). *Mongoose v8.x — Schema Guide*. https://mongoosejs.com/docs/guide.html

Elmasri, R., & Navathe, S. B. (2015). *Fundamentals of Database Systems* (7e éd.). Pearson. ISBN 978-0133970777.

Stripe Inc. (2026). *Stripe API — PaymentIntent metadata*. https://stripe.com/docs/api/payment_intents/object#payment_intent_object-metadata
