# 📐 Architecture Générale — Backend StreamMG

> [!abstract] Rôle
> API REST **stateless** unique, consommée par 2 clients (mobile + web). Toute la logique métier, sécurité, et accès aux données passe exclusivement par ce backend.

---

## 🗺️ Vue d'ensemble système

```mermaid
graph TB
    subgraph Clients
        M1["📱 App Mobile\nReact Native / Expo\nMembre 1"]
        M2["🌐 App Web\nReact.js / Vite\nMembre 2"]
    end

    subgraph Backend["🖥️ Backend — Membre 3"]
        API["API REST\nNode.js v20 + Express.js v4"]
        
        subgraph Middlewares
            AUTH["🔑 auth.js\nJWT decode"]
            ACCESS["🛡️ checkAccess\nfree|premium|paid"]
            HLS_MW["🎬 hlsTokenizer\ntoken + fingerprint"]
            THUMB["🖼️ validateThumbnail\nMulter required"]
            ROLE["👤 requireRole\nadmin|provider"]
        end

        subgraph Services
            FFMPEG["⚙️ ffmpegService\nMP4 → HLS .ts"]
            CRYPTO["🔐 cryptoService\nAES-256, tokens"]
            STRIPE_SVC["💳 stripeService\nPaymentIntent"]
        end
    end

    subgraph Storage
        MONGO[("🗄️ MongoDB Atlas\n8 collections")]
        FILES["📁 /uploads/\nthumbnails\nhls segments\naudio\nprivate"]
        STRIPE_API["💳 Stripe API\nmode test"]
    end

    M1 -->|"HTTPS + JWT"| API
    M2 -->|"HTTPS + JWT"| API
    API --> Middlewares
    Middlewares --> Services
    Services --> MONGO
    Services --> FILES
    Services --> STRIPE_API
```

---

## 🗂️ Structure des fichiers

```
backend/
├── 📄 server.js              ← Point d'entrée, port, démarrage
├── 📄 app.js                 ← Config Express, middlewares globaux
├── 📄 .env                   ← Variables d'environnement
│
├── 📁 config/
│   ├── database.js           ← Connexion MongoDB Atlas
│   ├── multer.js             ← Upload config (thumbnail OBLIGATOIRE)
│   └── stripe.js             ← Instance Stripe SDK
│
├── 📁 models/                ← 8 Schémas Mongoose
│   ├── User.js
│   ├── Content.js            ← thumbnail: required: true ⚠️
│   ├── RefreshToken.js       ← TTL index auto-purge
│   ├── Purchase.js           ← index unique {userId, contentId}
│   ├── Transaction.js
│   ├── WatchHistory.js
│   ├── TutorialProgress.js
│   └── Playlist.js
│
├── 📁 middlewares/
│   ├── auth.js               ← JWT → req.user
│   ├── checkAccess.js        ← ⭐ Logique freemium centrale
│   ├── hlsTokenizer.js       ← Token HLS + fingerprint SHA-256
│   ├── requireRole.js        ← admin / provider
│   ├── validateThumbnail.js  ← req.files.thumbnail obligatoire
│   └── errorHandler.js       ← Gestionnaire d'erreurs global
│
├── 📁 controllers/
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
├── 📁 routes/
│   └── [*.routes.js]         ← 1 fichier par domaine
│
├── 📁 services/
│   ├── ffmpegService.js      ← Pipeline transcoding HLS
│   ├── cryptoService.js      ← AES, tokens, fingerprint
│   └── stripeService.js      ← PaymentIntent logic
│
└── 📁 uploads/
    ├── thumbnails/           ← ✅ Accès public
    ├── hls/<contentId>/      ← 🔒 Token requis
    ├── audio/                ← ✅ Accès public
    └── private/              ← ❌ Jamais accessible directement
```

---

## 🔧 Stack technologique complète

```mermaid
mindmap
  root((Backend\nStreamMG))
    Runtime
      Node.js v20 LTS
      Express.js v4
    Base de données
      MongoDB Atlas M0
      Mongoose v8 ODM
    Authentification
      jsonwebtoken v9
      bcryptjs coût 12
    Upload & Media
      Multer v1
      fluent-ffmpeg
      music-metadata v10
    Cryptographie
      crypto natif Node.js
      AES-256-GCM
      SHA-256 fingerprint
    Paiement
      Stripe SDK v14
      PaymentIntent
      Webhooks
    Sécurité
      Helmet v7
      CORS
      express-rate-limit
      express-validator
    Infrastructure
      Railway hébergement
      Nginx reverse proxy
      Let's Encrypt SSL
      MongoDB Atlas
```

---

## ⚙️ Variables d'environnement

> [!tip] Fichier `.env` à créer à la racine du projet

```env
# ── Serveur ──────────────────────────────────
PORT=3001
NODE_ENV=development

# ── MongoDB ──────────────────────────────────
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/streamMG

# ── JWT ──────────────────────────────────────
JWT_SECRET=<256_bits_aléatoires>
JWT_EXPIRY=15m
REFRESH_TOKEN_EXPIRY=7d

# ── HLS Tokens ───────────────────────────────
HLS_TOKEN_SECRET=<secret_hls>
HLS_TOKEN_EXPIRY=600        # 10 minutes

# ── AES Download ─────────────────────────────
SIGNED_URL_SECRET=<secret_url>
SIGNED_URL_EXPIRY=900       # 15 minutes

# ── Stripe ───────────────────────────────────
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# ── CORS ─────────────────────────────────────
ALLOWED_ORIGINS=http://localhost:5173,https://streamMG.vercel.app

# ── Limites Upload ────────────────────────────
MAX_THUMBNAIL_SIZE=5242880   # 5 Mo
MAX_VIDEO_SIZE=524288000     # 500 Mo
```

---

## 📡 Routes — Vue d'ensemble

| Préfixe | Fichier | Auth | Description |
|---|---|---|---|
| `/api/auth` | auth.routes.js | Public | Inscription, connexion, refresh |
| `/api/contents` | content.routes.js | Mixte | Catalogue public + accès protégé |
| `/api/hls` | hls.routes.js | JWT + checkAccess | Streaming vidéo |
| `/api/download` | download.routes.js | JWT + checkAccess | Clé AES mobile |
| `/api/history` | history.routes.js | JWT | Historique de visionnage |
| `/api/tutorial` | tutorial.routes.js | JWT | Progression tutoriels |
| `/api/payment` | payment.routes.js | JWT / Stripe sig | Abonnement + achat |
| `/api/provider` | provider.routes.js | JWT + provider | Espace fournisseur |
| `/api/admin` | admin.routes.js | JWT + admin | Administration |

---

*Voir aussi : [[🛡️ Middlewares]] · [[📡 Contrat API — Endpoints]] · [[🗄️ Schémas MongoDB]]*
