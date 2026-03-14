# 📊 03 — Diagrammes UML

---

## Diagramme de classes — Backend

```mermaid
classDiagram
    class User {
        +ObjectId _id
        +String username
        +String email
        +String passwordHash
        +String role
        +Boolean isPremium
        +Date premiumExpiry
        +comparePassword(pwd) Boolean
        +toSafeObject() Object
    }

    class Content {
        +ObjectId _id
        +String title
        +String thumbnail ⚠️OBLIGATOIRE
        +String accessType
        +Number price
        +Boolean isTutorial
        +String hlsPath
        +Array lessons
        +ObjectId providerId
        +Boolean isPublished
        +Number viewCount
    }

    class RefreshToken {
        +ObjectId _id
        +ObjectId userId
        +String tokenHash
        +Date expiresAt
    }

    class Purchase {
        +ObjectId _id
        +ObjectId userId
        +ObjectId contentId
        +String stripePaymentId
        +Number amount
        +Date purchasedAt
    }

    class Transaction {
        +ObjectId _id
        +ObjectId userId
        +String type
        +String stripePaymentId
        +Number amount
        +String plan
        +String status
    }

    class WatchHistory {
        +ObjectId _id
        +ObjectId userId
        +ObjectId contentId
        +Number progress
        +Boolean completed
        +Date watchedAt
    }

    class TutorialProgress {
        +ObjectId _id
        +ObjectId userId
        +ObjectId contentId
        +Array completedLessons
        +Number percentComplete
        +Date lastUpdatedAt
        +calculatePercent() Number
    }

    class CryptoService {
        +generateHlsToken(payload) String
        +verifyHlsToken(token) Object
        +computeFingerprint(req) String
        +generateAesKey() String
        +generateIv() String
        +signDownloadUrl(path, exp) String
        +verifySignedUrl(url, sig) Boolean
    }

    class FfmpegService {
        +transcodeToHls(inputPath, outputDir) Promise
        +getVideoDuration(path) Number
        +extractCoverArt(audioPath) String
    }

    class StripeService {
        +createSubscriptionIntent(userId, plan) Object
        +createPurchaseIntent(userId, contentId) Object
        +handleWebhookEvent(event) Promise
        +verifyWebhookSignature(payload, sig) Object
    }

    class CheckAccessMiddleware {
        +checkAccess(req, res, next)
        -handleFree(next)
        -handlePremium(user, next)
        -handlePaid(user, contentId, price, next)
    }

    class HlsTokenizerMiddleware {
        +generateToken(req, res, next)
        +verifyToken(req, res, next)
        -extractFingerprint(req) String
    }

    User "1" --> "*" RefreshToken : possède
    User "1" --> "*" Purchase : effectue
    User "1" --> "*" Transaction : génère
    User "1" --> "*" WatchHistory : regarde
    User "1" --> "*" TutorialProgress : progresse
    User "1" --> "*" Content : fournit
    Content "1" --> "*" Purchase : vendu dans
    Content "1" --> "*" WatchHistory : visionné dans
    Content "1" --> "*" TutorialProgress : suivi dans
    CheckAccessMiddleware ..> Purchase : vérifie
    CheckAccessMiddleware ..> Content : consulte
    HlsTokenizerMiddleware ..> CryptoService : utilise
```

---

## Séquence — Authentification et Refresh Token

```mermaid
sequenceDiagram
    participant C as Client
    participant A as AuthController
    participant DB_U as MongoDB users
    participant DB_R as MongoDB refreshTokens

    C->>A: POST /auth/login { email, password }
    A->>DB_U: findOne({ email })
    DB_U-->>A: user document
    A->>A: bcrypt.compare(pwd, passwordHash)
    Note over A: ✅ match

    A->>A: jwt.sign(payload, JWT_SECRET, 15m) → JWT
    A->>A: crypto.randomBytes(32) → rawToken
    A->>A: bcrypt.hash(rawToken, 12) → tokenHash
    A->>DB_R: create({ userId, tokenHash, expiresAt: +7j })
    DB_R-->>A: saved

    A-->>C: 200 { token: JWT }\nSet-Cookie: refreshToken=rawToken (httpOnly)

    Note over C: --- 16 minutes plus tard ---

    C->>A: GET /protected (JWT expiré)
    A-->>C: 401 Token expiré

    Note over C: Intercepteur axios déclenché
    C->>A: POST /auth/refresh\nCookie: refreshToken=rawToken
    A->>DB_R: findOne({ userId })
    DB_R-->>A: [{ tokenHash }]
    A->>A: bcrypt.compare(rawToken, tokenHash) → TRUE
    A->>DB_R: deleteOne(ancien doc)
    A->>A: générer nouveau rawToken + tokenHash
    A->>DB_R: create(nouveau doc)
    A->>A: jwt.sign(...) → nouveauJWT
    A-->>C: 200 { token: nouveauJWT }\nSet-Cookie: nouveau rawToken

    C->>A: GET /protected (nouveauJWT) [rejouée automatiquement]
    A-->>C: 200 ✅
```

---

## Séquence — Lecture HLS protégée (web)

```mermaid
sequenceDiagram
    participant HLS as hls.js Frontend
    participant API as Backend API
    participant MW as hlsTokenizer
    participant FS as /uploads/hls/

    HLS->>API: GET /hls/:id/token\nBearer JWT
    API->>API: auth → req.user
    API->>API: checkAccess(content)\n→ accessType vérifié

    API->>API: sha256(User-Agent + IP + sessionId)\n→ fingerprintHash
    API->>API: jwt.sign({contentId, userId,\nfingerprintHash, exp:+10min})\n→ hlsToken

    API-->>HLS: 200 { hlsUrl: "/hls/:id/index.m3u8?token=eyJ..." }

    HLS->>FS: GET /hls/:id/index.m3u8?token=eyJ...
    FS->>MW: verifyHlsToken(token)
    MW->>MW: computeFingerprint(req)
    MW->>MW: compare → MATCH ✅
    FS-->>HLS: 200 manifest M3U8

    loop Pour chaque segment (toutes les 10s)
        HLS->>FS: GET /hls/:id/seg00N.ts?token=eyJ...
        FS->>MW: verifyHlsToken + fingerprint
        MW-->>FS: ✅ next()
        FS-->>HLS: 200 binaire .ts
    end

    Note over HLS: IDM/JDownloader copie l'URL
    HLS->>FS: GET /hls/:id/seg001.ts?token=eyJ... (autre UA)
    FS->>MW: computeFingerprint → DIFFÉRENT ❌
    MW-->>HLS: 403 Forbidden
```

---

## Séquence — Achat unitaire (Stripe)

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant API as Backend
    participant STR as Stripe API
    participant DB as MongoDB

    FE->>API: POST /payment/purchase { contentId }
    API->>API: auth → req.user
    API->>DB: Purchase.findOne({userId, contentId})
    DB-->>API: null (pas encore acheté)

    API->>STR: paymentIntents.create({\namount, currency: "mga",\nmetadata: { type:"purchase",\nuserId, contentId }})
    STR-->>API: { clientSecret }
    API-->>FE: 200 { clientSecret }

    FE->>STR: confirmPayment(clientSecret, card 4242...)
    STR-->>FE: succès

    Note over STR,API: Webhook asynchrone
    STR->>API: POST /payment/webhook\npayment_intent.succeeded
    API->>API: stripe.webhooks.constructEvent()\n→ vérification signature
    API->>API: metadata.type === "purchase" ?

    API->>DB: Purchase.create({userId, contentId,\nstripePaymentId, amount})
    Note over DB: Index unique → idempotence
    API->>DB: Transaction.create({...})
    DB-->>API: ✅ créé

    Note over FE: Prochain accès
    FE->>API: GET /hls/:id/token
    API->>API: checkAccess → accessType: "paid"
    API->>DB: Purchase.findOne({userId, contentId})
    DB-->>API: purchase ✅ trouvé
    API-->>FE: 200 { hlsUrl }
```

---

## Séquence — checkAccess (cas Premium sur contenu Payant)

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant MW as checkAccess
    participant DB as MongoDB purchases

    Note over FE,DB: Cas critique soutenance ⚠️
    FE->>MW: GET /hls/:id/token\nJWT role="premium"
    MW->>MW: content.accessType = "paid"
    MW->>MW: req.user.role = "premium"
    Note over MW: ⚠️ Le rôle premium\nNE suffit PAS pour "paid"
    MW->>DB: Purchase.findOne({userId, contentId})
    DB-->>MW: null (aucun achat)
    MW-->>FE: 403 { reason: "purchase_required",\nprice: 800000 }

    Note over FE: Même écran d'achat\nque pour un utilisateur standard
```

---

## Diagramme de cas d'utilisation

```mermaid
graph LR
    subgraph ACTEURS
        V((Visiteur))
        U((User\nstandard))
        P((Premium))
        PR((Provider))
        A((Admin))
    end

    subgraph AUTH["🔐 Auth"]
        R[S'inscrire]
        L[Se connecter]
        RF[Refresh JWT]
    end

    subgraph CATALOGUE["📚 Catalogue"]
        BR[Parcourir]
        SR[Rechercher]
        DT[Détail contenu]
    end

    subgraph LECTURE["🎬 Lecture"]
        FR[Lire gratuit]
        PMR[Lire premium]
        PR2[Lire payant]
        TR[Tutoriel + progression]
    end

    subgraph PAIEMENT["💳 Paiement"]
        SB[S'abonner Premium]
        BY[Acheter contenu]
    end

    subgraph PROVIDER["🎥 Provider"]
        UP[Uploader contenu\n+ thumbnail ⚠️]
        MG[Gérer ses contenus]
    end

    subgraph ADMIN["⚙️ Admin"]
        VA[Valider contenu]
        ST[Statistiques]
        GU[Gérer users]
    end

    V --> R
    V --> L
    V --> BR
    V --> FR
    U --> SR
    U --> DT
    U --> PMR
    U --> BY
    U --> PR2
    U --> RF
    U --> TR
    P --> PMR
    P --> BY
    P --> PR2
    PR --> UP
    PR --> MG
    A --> VA
    A --> ST
    A --> GU

    style AUTH fill:#1e3a5f,stroke:#4a9ede,color:#fff
    style CATALOGUE fill:#1a3a1a,stroke:#4ade80,color:#fff
    style LECTURE fill:#2d1b4e,stroke:#a855f7,color:#fff
    style PAIEMENT fill:#3a2a0a,stroke:#fbbf24,color:#fff
    style PROVIDER fill:#1a2a3a,stroke:#67e8f9,color:#fff
    style ADMIN fill:#3a1a1a,stroke:#f87171,color:#fff
```

> [!tip] Retour
> ← [[🏠 INDEX — StreamMG Backend]]
