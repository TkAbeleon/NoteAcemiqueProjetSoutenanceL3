# 🏗️ 01 — Architecture Générale

> [!abstract] Résumé
> API REST stateless, pattern **multi-client avec backend partagé**. Deux frontends (mobile + web) consomment la même API. MongoDB géré exclusivement côté backend.

---

## Architecture globale

```mermaid
graph TB
    subgraph CLIENT["📱 Clients"]
        M1["App Mobile\nReact Native + Expo 52\nMembre 1"]
        M2["App Web\nReact.js + Vite 5\nMembre 2"]
    end

    subgraph BACKEND["⚙️ Backend — Membre 3"]
        API["API REST\nNode.js v20 + Express v4"]
        MW["Middlewares\nauth · checkAccess · hlsTokenizer\nMulter · requireRole"]
        SVC["Services\nffmpegService · cryptoService · stripeService"]
    end

    subgraph DATA["💾 Données"]
        DB[("MongoDB Atlas\n8 collections")]
        FILES["Fichiers\n/thumbnails\n/hls segments\n/audio\n/private (caché)"]
        STRIPE["Stripe API\nmode test"]
    end

    M1 -->|"HTTPS + JWT"| API
    M2 -->|"HTTPS + JWT"| API
    API --> MW
    MW --> SVC
    SVC --> DB
    SVC --> FILES
    SVC --> STRIPE

    style CLIENT fill:#1e3a5f,stroke:#4a9ede,color:#fff
    style BACKEND fill:#1a3a1a,stroke:#4ade80,color:#fff
    style DATA fill:#3a1a1a,stroke:#f87171,color:#fff
```

---

## Stack technologique

```mermaid
graph LR
    subgraph RUNTIME["Runtime"]
        NODE["Node.js v20 LTS"]
        EXPRESS["Express.js v4"]
    end

    subgraph AUTH["Authentification"]
        JWT["jsonwebtoken v9\nJWT HS256 · 15min"]
        BCRYPT["bcryptjs\ncoût 12"]
    end

    subgraph MEDIA["Traitement Média"]
        FFMPEG["fluent-ffmpeg\nMP4 → HLS .ts"]
        MUSIC["music-metadata v10\nID3 extraction"]
        MULTER["Multer v1\nUpload fichiers"]
    end

    subgraph CRYPTO["Cryptographie"]
        NODECRYPTO["Node.js crypto (natif)\nAES-256 · tokens · fingerprint"]
    end

    subgraph PAYMENT["Paiement"]
        STRIPE["Stripe SDK v14\nPaymentIntent · Webhook"]
    end

    subgraph SECURITY["Sécurité"]
        HELMET["Helmet v7\nHeaders HTTP"]
        CORS["cors\n2 origines"]
        RATELIMIT["express-rate-limit v7\n10/15min auth"]
        VALIDATOR["express-validator v7"]
    end

    subgraph DB_ORM["Base de données"]
        MONGOOSE["Mongoose v8\nODM + validation"]
        ATLAS["MongoDB Atlas\ncluster M0"]
    end

    style AUTH fill:#1e3a5f,stroke:#4a9ede,color:#fff
    style MEDIA fill:#2d1b4e,stroke:#a855f7,color:#fff
    style CRYPTO fill:#1a3a2a,stroke:#4ade80,color:#fff
    style PAYMENT fill:#3a2a0a,stroke:#fbbf24,color:#fff
    style SECURITY fill:#3a1a1a,stroke:#f87171,color:#fff
```

---

## Structure des fichiers

```
backend/
├── 📄 server.js                   ← Point d'entrée, écoute PORT
├── 📄 app.js                      ← Config Express + middlewares globaux
├── 📄 .env                        ← Variables d'environnement
│
├── 📁 config/
│   ├── database.js                ← Connexion MongoDB Atlas
│   ├── multer.js                  ← Config upload multipart
│   └── stripe.js                  ← Instance Stripe SDK
│
├── 📁 models/                     ← 8 schémas Mongoose
│   ├── User.js
│   ├── Content.js                 ← thumbnail: required: true ⚠️
│   ├── RefreshToken.js
│   ├── Purchase.js                ← index unique {userId, contentId}
│   ├── Transaction.js
│   ├── WatchHistory.js
│   ├── TutorialProgress.js
│   └── Playlist.js
│
├── 📁 middlewares/
│   ├── auth.js                    ← Décode JWT → req.user
│   ├── checkAccess.js             ← 🔑 Logique d'accès freemium
│   ├── hlsTokenizer.js            ← 🎬 Token HLS + fingerprint
│   ├── requireRole.js             ← admin / provider
│   ├── validateThumbnail.js       ← 🖼️ Vignette obligatoire
│   └── errorHandler.js            ← Erreurs globales
│
├── 📁 controllers/                ← Logique métier par domaine
│   ├── authController.js
│   ├── contentController.js
│   ├── hlsController.js
│   ├── downloadController.js
│   ├── historyController.js
│   ├── tutorialController.js
│   ├── paymentController.js
│   ├── providerController.js
│   └── adminController.js
│
├── 📁 routes/                     ← Déclaration des routes Express
│   └── *.routes.js (9 fichiers)
│
├── 📁 services/
│   ├── ffmpegService.js           ← Pipeline transcoding HLS
│   ├── cryptoService.js           ← AES-256, tokens, fingerprint
│   └── stripeService.js           ← Logique PaymentIntent
│
└── 📁 uploads/
    ├── thumbnails/                ← ✅ Accès public
    ├── hls/<contentId>/           ← ✅ Accès avec token HLS
    ├── audio/                     ← ✅ Accès public
    └── private/                   ← 🚫 JAMAIS accessible via route
```

---

## Variables d'environnement

```env
# Serveur
PORT=3001
NODE_ENV=production

# Base de données
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/streamMG

# JWT
JWT_SECRET=secret_256bits_très_long_et_aléatoire
JWT_EXPIRY=15m
REFRESH_TOKEN_EXPIRY=7d

# HLS
HLS_TOKEN_SECRET=autre_secret_pour_hls
HLS_TOKEN_EXPIRY=600        # 10 minutes

# AES Download
SIGNED_URL_SECRET=secret_url_signée
SIGNED_URL_EXPIRY=900       # 15 minutes

# Stripe (mode test)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# CORS (2 origines autorisées)
ALLOWED_ORIGINS=http://localhost:5173,https://streamMG.vercel.app
```

> [!tip] Retour
> ← [[🏠 INDEX — StreamMG Backend]]
