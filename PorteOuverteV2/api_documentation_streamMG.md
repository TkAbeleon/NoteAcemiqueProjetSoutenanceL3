# 📖 Documentation de l'API — StreamMG

**Version :** 1.0  
**Date :** Février 2026  
**Base URL (production) :** `https://api.streamMG.railway.app/api`  
**Base URL (développement) :** `http://localhost:3001/api`  
**Format :** JSON exclusivement  
**Auth :** Header `Authorization: Bearer <JWT>` pour toutes les routes protégées

> **Note cross-platform :** Le mobile (React Native/Expo) et le web (React.js/Vite) consomment la **même API REST**. Les comportements, réponses et codes d'erreur sont identiques sur les deux plateformes. Seul le stockage du refresh token diffère : cookie `httpOnly` sur web, `expo-secure-store` sur mobile.

---

## 🛡️ Types Communs

Ces types sont partagés et réutilisés dans toute la documentation.

```typescript
// Niveaux d'accès d'un contenu
type AccessType = "free" | "premium" | "paid";

// Rôles utilisateur
type UserRole = "user" | "premium" | "provider" | "admin";

// Types de contenu
type ContentType = "video" | "audio";

// Catégories disponibles
type ContentCategory =
  | "film"
  | "salegy"
  | "hira_gasy"
  | "tsapiky"
  | "beko"
  | "documentaire"
  | "podcast"
  | "autre";

// Langues disponibles
type Language = "mg" | "fr" | "en";

// Plans d'abonnement
type SubscriptionPlan = "monthly" | "annual";

// Raisons de refus d'accès — renvoyées par le middleware checkAccess
type AccessDeniedReason =
  | "subscription_required"
  | "purchase_required"
  | "login_required";

// Format standard d'une erreur 403 checkAccess
interface AccessDeniedError {
  reason: AccessDeniedReason;
  price?: number; // présent uniquement si reason === "purchase_required"
}

// Format standard d'une erreur générique
interface ApiError {
  message: string;
  code: string;
}
```

### Codes HTTP standard

| Code | Signification |
|---|---|
| `200` | Succès |
| `201` | Ressource créée |
| `400` | Données invalides (vignette absente, MIME incorrect, champ manquant) |
| `401` | Token absent, expiré ou invalide |
| `403` | Accès refusé (rôle insuffisant, contenu protégé, token HLS invalide) |
| `404` | Ressource introuvable |
| `409` | Conflit (email dupliqué, achat déjà effectué) |
| `429` | Rate limit dépassé |
| `500` | Erreur serveur interne |

---

## 🔐 Écran : Authentification

Cette section couvre l'inscription, la connexion, le renouvellement de session et la déconnexion. Ces écrans sont présents sur mobile et web avec un comportement identique.

---

### 1. Inscription

- **Description :** Crée un nouveau compte utilisateur. Le mot de passe est haché avec bcrypt (coût 12). Le rôle par défaut est `"user"`, `isPremium` est `false`.
- **Requête :** `POST /auth/register`
- **Accès :** Public
- **Rate limit :** 10 requêtes / 15 min par IP

```typescript
// Body
interface RegisterDTO {
  username: string; // 3–30 caractères, alphanumérique
  email: string;    // format email valide
  password: string; // minimum 8 caractères
}

// Réponse 201
interface RegisterResponse {
  token: string;
  user: {
    _id: string;
    username: string;
    email: string;
    role: UserRole;     // toujours "user" à l'inscription
    isPremium: boolean; // toujours false à l'inscription
  };
}

// Erreurs
// 409 → { message: "Email déjà utilisé", code: "EMAIL_DUPLICATE" }
// 400 → { message: "Mot de passe trop faible (minimum 8 caractères)", code: "WEAK_PASSWORD" }
```

**Exemple body :**
```json
{ "username": "Rabe", "email": "rabe@exemple.mg", "password": "MotDePasse1" }
```

**Exemple réponse (201) :**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "65f3a2b4c8e9d1234567890a",
    "username": "Rabe",
    "email": "rabe@exemple.mg",
    "role": "user",
    "isPremium": false
  }
}
```

---

### 2. Connexion

- **Description :** Authentifie l'utilisateur et retourne un JWT (15 min) et un refresh token (7 jours). Sur web, le refresh token est émis en cookie `httpOnly`. Sur mobile, il est inclus dans le corps de la réponse.
- **Requête :** `POST /auth/login`
- **Accès :** Public
- **Rate limit :** 10 requêtes / 15 min par IP

```typescript
// Body
interface LoginDTO {
  email: string;
  password: string;
}

// Réponse 200 — Web (refresh token en cookie httpOnly, absent du body)
interface LoginResponseWeb {
  token: string;
  user: {
    _id: string;
    username: string;
    role: UserRole;
    isPremium: boolean;
    premiumExpiry: string | null; // ISO 8601, null si non premium
  };
}

// Réponse 200 — Mobile (refresh token inclus dans le body)
interface LoginResponseMobile extends LoginResponseWeb {
  refreshToken: string; // à stocker dans expo-secure-store
}

// Erreurs
// 401 → { message: "Email ou mot de passe incorrect", code: "INVALID_CREDENTIALS" }
// 429 → { message: "Trop de tentatives. Réessayez dans 15 minutes.", code: "RATE_LIMIT" }
```

**Exemple réponse (200) :**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "_id": "65f3a2b4c8e9d1234567890a",
    "username": "Rabe",
    "role": "premium",
    "isPremium": true,
    "premiumExpiry": "2026-03-15T00:00:00.000Z"
  }
}
```

---

### 3. Renouvellement du JWT (Refresh)

- **Description :** Émet un nouveau JWT et invalide l'ancien refresh token (rotation systématique). Appelé automatiquement par l'intercepteur axios en cas de 401.
- **Requête :** `POST /auth/refresh`
- **Accès :** Cookie `httpOnly` (web) ou refresh token dans le body (mobile)

```typescript
// Body — Mobile uniquement (le web envoie le cookie automatiquement)
interface RefreshDTO {
  refreshToken: string;
}

// Réponse 200 — Web
interface RefreshResponseWeb {
  token: string; // nouveau JWT
}

// Réponse 200 — Mobile
interface RefreshResponseMobile {
  token: string;
  refreshToken: string; // nouveau refresh token — remplace l'ancien dans expo-secure-store
}

// Erreurs
// 401 → { message: "Refresh token invalide ou expiré", code: "INVALID_REFRESH_TOKEN" }
```

---

### 4. Déconnexion

- **Description :** Invalide le refresh token en base. Le JWT en mémoire (zustand) doit être supprimé côté client.
- **Requête :** `POST /auth/logout`
- **Accès :** JWT requis

```typescript
// Body — aucun

// Réponse 200
interface LogoutResponse {
  message: string; // "Déconnecté avec succès"
}
```

---

## 🏠 Écran : Catalogue (Accueil)

Écran principal affiché à tous les utilisateurs (visiteurs inclus). Chaque contenu possède obligatoirement une vignette (`thumbnail` jamais null). Les badges visuels indiquent le niveau d'accès.

---

### 1. Lister les contenus (catalogue paginé)

- **Description :** Retourne la liste paginée des contenus publiés avec filtres optionnels.
- **Requête :** `GET /contents`
- **Accès :** Public

```typescript
// Query params
interface ContentsQueryParams {
  page?: number;              // défaut : 1
  limit?: number;             // défaut : 20, max : 50
  type?: ContentType;
  category?: ContentCategory;
  accessType?: AccessType;
  isTutorial?: boolean;
  search?: string;            // recherche sur titre, artiste, description
}

// Un item du catalogue
interface ContentSummary {
  _id: string;
  title: string;
  type: ContentType;
  category: ContentCategory;
  thumbnail: string;    // jamais null — chemin vers /uploads/thumbnails/
  duration: number;     // en secondes
  accessType: AccessType;
  price: number | null; // null si free ou premium
  isTutorial: boolean;
  artist: string | null;
  viewCount: number;
  isPublished: boolean;
}

// Réponse 200
interface ContentsResponse {
  contents: ContentSummary[];
  total: number;
  page: number;
  pages: number;
}
```

**Exemple réponse (200) :**
```json
{
  "contents": [
    {
      "_id": "65f3a2b4c8e9d1234567890b",
      "title": "Mora Mora",
      "type": "audio",
      "category": "salegy",
      "thumbnail": "/uploads/thumbnails/mora_mora_e1f4a.jpg",
      "duration": 243,
      "accessType": "free",
      "price": null,
      "isTutorial": false,
      "artist": "Tarika Sammy",
      "viewCount": 1842,
      "isPublished": true
    }
  ],
  "total": 148,
  "page": 1,
  "pages": 8
}
```

---

### 2. Contenus mis en avant

- **Description :** Retourne les contenus sélectionnés manuellement par l'administrateur pour la section "À la une".
- **Requête :** `GET /contents/featured`
- **Accès :** Public

```typescript
// Réponse 200
interface FeaturedResponse {
  featured: ContentSummary[];
}
```

---

### 3. Contenus tendance (Top 10)

- **Description :** Retourne les 10 contenus les plus vus sur les 7 derniers jours.
- **Requête :** `GET /contents/trending`
- **Accès :** Public

```typescript
// Item tendance — étend ContentSummary avec un classement
interface TrendingItem extends ContentSummary {
  rank: number; // 1 à 10
}

// Réponse 200
interface TrendingResponse {
  trending: TrendingItem[];
}
```

---

### 4. Détail d'un contenu

- **Description :** Retourne toutes les métadonnées d'un contenu. Ne retourne pas d'URL de lecture — celle-ci est obtenue via `/hls/:id/token` ou `/audio/:id/url`.
- **Requête :** `GET /contents/:id`
- **Accès :** Public

```typescript
// Réponse 200
interface ContentDetail {
  _id: string;
  title: string;
  description: string;
  type: ContentType;
  category: ContentCategory;
  thumbnail: string;    // jamais null
  duration: number;     // en secondes
  accessType: AccessType;
  price: number | null;
  isTutorial: boolean;
  artist: string | null;
  album: string | null;
  language: Language;
  viewCount: number;
  provider: {
    _id: string;
    username: string;
  };
  createdAt: string;    // ISO 8601
}

// Erreurs
// 404 → { message: "Contenu introuvable", code: "CONTENT_NOT_FOUND" }
```

---

### 5. Incrémenter le compteur de vues

- **Description :** Appelé automatiquement au démarrage du lecteur.
- **Requête :** `POST /contents/:id/view`
- **Accès :** Public

```typescript
// Body — aucun

// Réponse 200
interface ViewResponse {
  viewCount: number;
}
```

---

## ▶️ Écran : Lecteur Vidéo (Streaming HLS)

Le lecteur vidéo est protégé par HLS avec tokens signés. Aucun fichier `.mp4` complet n'est jamais servi directement. Sur web, `hls.js` gère la lecture des segments `.ts`. Sur mobile, `expo-av` reçoit l'URL du manifest signé.

---

### 1. Obtenir le token HLS (URL de lecture)

- **Description :** Vérifie les droits (`checkAccess`) et génère un token HLS signé valable 10 minutes, incluant un fingerprint de session. C'est le **premier appel** avant toute lecture vidéo.
- **Requête :** `GET /hls/:id/token`
- **Accès :** JWT + `checkAccess`

```typescript
// Réponse 200
interface HlsTokenResponse {
  hlsUrl: string;    // URL du manifest signé : /hls/:id/index.m3u8?token=eyJ...
  expiresIn: number; // en secondes, toujours 600 (10 min)
}

// Erreurs
// 401 → { message: "Token JWT absent ou invalide", code: "UNAUTHORIZED" }
// 403 → AccessDeniedError
// 404 → { message: "Contenu introuvable", code: "CONTENT_NOT_FOUND" }
```

**Exemple réponse (200) :**
```json
{
  "hlsUrl": "/hls/65f3a2b4c8e9d1234567890b/index.m3u8?token=eyJhbGci...",
  "expiresIn": 600
}
```

> **Web :** `hls.js` est configuré avec `hlsUrl`. En cas d'erreur 403 sur un segment, le frontend redemande un token :
> ```typescript
> hls.on(Hls.Events.ERROR, async (event, data) => {
>   if (data.response?.code === 403) {
>     const { hlsUrl }: HlsTokenResponse = await api.get(`/hls/${contentId}/token`);
>     hls.loadSource(hlsUrl);
>   }
> });
> ```
> **Mobile :** `expo-av` reçoit `hlsUrl` directement comme source.

---

### 2. Manifest HLS

- **Description :** Retourne le manifest `index.m3u8` listant les segments `.ts`. Requiert le token dans l'URL.
- **Requête :** `GET /hls/:id/index.m3u8?token=<hlsToken>`
- **Accès :** Token HLS valide

```typescript
// Query params
interface HlsManifestParams {
  token: string; // token signé obtenu via /hls/:id/token
}

// Réponse 200 : fichier texte .m3u8 (Content-Type: application/vnd.apple.mpegurl)

// Erreurs
// 403 → { message: "Token HLS absent ou expiré", code: "HLS_TOKEN_INVALID" }
```

---

### 3. Segment vidéo (.ts)

- **Description :** Retourne un segment de 10 secondes. Le fingerprint (User-Agent + IP + cookie `sessionId`) est vérifié à **chaque requête**. Un fingerprint différent retourne 403 — ce qui bloque IDM, JDownloader et toute copie d'URL.
- **Requête :** `GET /hls/:id/:segment?token=<hlsToken>`
- **Accès :** Token HLS valide + fingerprint correspondant

```typescript
// Query params
interface HlsSegmentParams {
  token: string; // même token que le manifest
}

// Réponse 200 : données binaires du segment (Content-Type: video/MP2T)

// Erreurs
// 403 → { message: "Token HLS invalide ou fingerprint non correspondant", code: "HLS_FORBIDDEN" }
```

---

## 🎵 Écran : Lecteur Audio

L'audio est servi via URL signée (pas de HLS). L'accès est contrôlé par `checkAccess`. Le mini-player reste visible lors de la navigation sur les deux plateformes.

---

### 1. Obtenir l'URL de lecture audio

- **Description :** Vérifie les droits et retourne une URL signée temporaire (15 min) vers le fichier audio, ainsi que les métadonnées extraites via ID3.
- **Requête :** `GET /audio/:id/url`
- **Accès :** JWT + `checkAccess`

```typescript
// Réponse 200
interface AudioUrlResponse {
  audioUrl: string;   // URL signée temporaire vers le fichier audio
  expiresIn: number;  // en secondes, toujours 900 (15 min)
  metadata: {
    title: string;
    artist: string | null;
    album: string | null;
    duration: number;  // en secondes
    coverArt: string;  // pochette ID3 si disponible, sinon thumbnail du contenu
  };
}

// Erreurs
// 403 → AccessDeniedError
// 404 → { message: "Contenu audio introuvable", code: "AUDIO_NOT_FOUND" }
```

---

## 📥 Écran : Téléchargement Hors-Ligne (Mobile uniquement)

Le téléchargement hors-ligne est disponible **uniquement sur mobile**. Le fichier est chiffré localement (AES-256-GCM) et illisible hors de l'application.

---

### 1. Initier un téléchargement sécurisé

- **Description :** Vérifie les droits, génère une clé AES-256 et un IV uniques, et retourne une URL signée (15 min) vers le fichier source. La clé n'est **jamais stockée en base de données** — elle est transmise une seule fois.
- **Requête :** `POST /download/:id`
- **Accès :** JWT + `checkAccess`

```typescript
// Body — aucun

// Réponse 200
interface DownloadResponse {
  aesKeyHex: string;  // clé AES-256 — 64 caractères hex (32 octets)
  ivHex: string;      // vecteur d'initialisation — 32 caractères hex (16 octets)
  signedUrl: string;  // URL temporaire (15 min) vers le fichier source
  expiresIn: number;  // toujours 900
}

// Erreurs
// 403 → AccessDeniedError
// 409 → { message: "Ce contenu est déjà téléchargé", code: "ALREADY_DOWNLOADED" }
//         La clé n'est jamais retransmise une seconde fois.
```

> **Implémentation mobile :**
> ```typescript
> const { aesKeyHex, ivHex, signedUrl }: DownloadResponse =
>   await api.post(`/download/${contentId}`);
>
> // Téléchargement par chunks (4–8 Mo) via expo-file-system
> // Chiffrement immédiat de chaque chunk avec react-native-quick-crypto (AES-256-GCM)
> // Sauvegarde : FileSystem.documentDirectory + "offline/" + contentId + ".enc"
> await SecureStore.setItemAsync(`aes_${contentId}`, JSON.stringify({ aesKeyHex, ivHex }));
> ```

---

## 📚 Écran : Tutoriels

Les tutoriels sont des contenus organisés en séries de leçons ordonnées. La plateforme suit la progression de chaque utilisateur. Ils suivent le même système d'accès (`free`, `premium`, `paid`).

---

### 1. Leçons d'un tutoriel

- **Description :** Retourne la liste ordonnée des leçons d'un tutoriel.
- **Requête :** `GET /contents/:id/lessons`
- **Accès :** JWT + `checkAccess`

```typescript
// Une leçon
interface Lesson {
  index: number;
  title: string;
  duration: number;         // en secondes
  thumbnail: string | null; // vignette optionnelle par leçon
}

// Réponse 200
interface TutorialLessonsResponse {
  tutorialId: string;
  title: string;
  thumbnail: string;    // vignette du tutoriel — obligatoire, jamais null
  totalLessons: number;
  lessons: Lesson[];
}
```

**Exemple réponse (200) :**
```json
{
  "tutorialId": "65f3a2b4c8e9d1234567890d",
  "title": "Apprendre le salegy — Cours débutant",
  "thumbnail": "/uploads/thumbnails/tuto_salegy_cover_a3f9b.jpg",
  "totalLessons": 6,
  "lessons": [
    { "index": 0, "title": "Introduction au rythme salegy", "duration": 480, "thumbnail": "/uploads/thumbnails/lesson_0_opt.jpg" },
    { "index": 1, "title": "Techniques de base à la guitare", "duration": 620, "thumbnail": null }
  ]
}
```

---

### 2. Enregistrer la progression d'une leçon

- **Description :** Marque une leçon comme complétée et recalcule le pourcentage global. Appelé automatiquement lorsque l'utilisateur dépasse 90 % de la durée d'une leçon.
- **Requête :** `POST /tutorial/progress/:tutorialId`
- **Accès :** JWT requis

```typescript
// Body
interface TutorialProgressDTO {
  lessonIndex: number;  // index de la leçon terminée (base 0)
  completed: boolean;   // toujours true lors de cet appel
}

// Réponse 200
interface TutorialProgressResponse {
  tutorialId: string;
  completedLessons: number[];  // liste des index complétés
  percentComplete: number;     // 0 à 100, arrondi à 2 décimales
  lastLessonIndex: number;
  lastUpdatedAt: string;       // ISO 8601
}
```

---

### 3. Tutoriels en cours

- **Description :** Retourne les tutoriels non terminés (`percentComplete < 100`) de l'utilisateur, triés par date de dernière activité décroissante.
- **Requête :** `GET /tutorial/progress`
- **Accès :** JWT requis

```typescript
// Un tutoriel en cours
interface TutorialInProgress {
  contentId: {
    _id: string;
    title: string;
    thumbnail: string; // jamais null
  };
  lastLessonIndex: number;
  percentComplete: number;
  lastUpdatedAt: string; // ISO 8601
}

// Réponse 200
interface TutorialsInProgressResponse {
  inProgress: TutorialInProgress[];
}
```

---

## 📜 Écran : Historique de Lecture

---

### 1. Enregistrer une progression de lecture

- **Description :** Sauvegarde la position de lecture. Appelé toutes les 10 secondes pendant la lecture et à la fermeture du lecteur.
- **Requête :** `POST /history/:contentId`
- **Accès :** JWT requis

```typescript
// Body
interface HistoryDTO {
  progress: number;   // position actuelle en secondes
  duration: number;   // durée totale du contenu en secondes
  completed: boolean; // true si progress >= 90% de duration
}

// Réponse 200
interface HistoryResponse {
  message: string; // "Progression enregistrée"
}
```

---

### 2. Récupérer l'historique

- **Description :** Retourne les contenus récemment vus/écoutés avec leur position de reprise, triés par date décroissante.
- **Requête :** `GET /history`
- **Accès :** JWT requis

```typescript
// Un item d'historique
interface HistoryItem {
  _id: string;
  content: {
    _id: string;
    title: string;
    thumbnail: string; // jamais null
    type: ContentType;
    duration: number;
  };
  progress: number;    // position de reprise en secondes
  completed: boolean;
  watchedAt: string;   // ISO 8601
}

// Réponse 200
interface HistoryListResponse {
  history: HistoryItem[];
}
```

---

## 💳 Écran : Abonnement Premium

---

### 1. Créer un abonnement Premium

- **Description :** Crée un `PaymentIntent` Stripe. Le `clientSecret` est transmis à Stripe Elements (web) ou CardField (mobile) pour finaliser le paiement côté client.
- **Requête :** `POST /payment/subscribe`
- **Accès :** JWT requis

```typescript
// Body
interface SubscribeDTO {
  plan: SubscriptionPlan; // "monthly" | "annual"
}

// Réponse 200
interface SubscribeResponse {
  clientSecret: string; // transmis directement au Stripe SDK côté client
  amount: number;       // en centimes : 500000 (mensuel) ou 5000000 (annuel)
  currency: string;     // toujours "mga"
}

// Erreurs
// 400 → { message: "Plan invalide", code: "INVALID_PLAN" }
// 409 → { message: "Vous avez déjà un abonnement actif", code: "ALREADY_SUBSCRIBED" }
```

---

### 2. Statut de l'abonnement Premium

- **Description :** Retourne le statut Premium de l'utilisateur connecté.
- **Requête :** `GET /payment/status`
- **Accès :** JWT requis

```typescript
// Réponse 200
interface PremiumStatusResponse {
  isPremium: boolean;
  premiumExpiry: string | null; // ISO 8601, null si non premium
  plan: SubscriptionPlan | null;
}
```

---

## 🛒 Écran : Achat Unitaire (Contenu Payant)

L'achat unitaire est **indépendant de l'abonnement**. Un utilisateur Premium doit payer séparément les contenus de type `paid`. L'accès est permanent après achat.

---

### 1. Initier un achat unitaire

- **Description :** Crée un `PaymentIntent` Stripe pour un contenu payant. Vérifie l'absence d'un achat antérieur (idempotence).
- **Requête :** `POST /payment/purchase`
- **Accès :** JWT requis

```typescript
// Body
interface PurchaseDTO {
  contentId: string;
}

// Réponse 200
interface PurchaseResponse {
  clientSecret: string;  // transmis directement au Stripe SDK côté client
  amount: number;        // prix du contenu en centimes
  currency: string;      // toujours "mga"
  contentTitle: string;  // titre affiché dans la modale de confirmation
}

// Erreurs
// 404 → { message: "Contenu introuvable", code: "CONTENT_NOT_FOUND" }
// 409 → { message: "Vous avez déjà acheté ce contenu", code: "ALREADY_PURCHASED" }
```

---

### 2. Liste des achats de l'utilisateur

- **Description :** Retourne tous les contenus achetés définitivement par l'utilisateur connecté.
- **Requête :** `GET /payment/purchases`
- **Accès :** JWT requis

```typescript
// Un achat
interface PurchaseItem {
  _id: string;
  contentId: {
    _id: string;
    title: string;
    thumbnail: string; // jamais null
    type: ContentType;
    duration: number;
  };
  amount: number;      // prix payé au moment de l'achat, en centimes
  purchasedAt: string; // ISO 8601
}

// Réponse 200
interface PurchasesListResponse {
  purchases: PurchaseItem[];
}
```

---

### 3. Webhook Stripe (événements de paiement)

- **Description :** Reçoit les événements Stripe. La signature est vérifiée à chaque appel via le header `stripe-signature`. Distingue abonnement et achat unitaire via `metadata.type`.
- **Requête :** `POST /payment/webhook`
- **Accès :** Signature Stripe (header `stripe-signature`)

```typescript
// Réponse 200 (succès de traitement)
interface WebhookResponse {
  received: boolean; // toujours true si traitement OK
}

// Erreurs
// 400 → { message: "Signature Stripe invalide", code: "INVALID_STRIPE_SIGNATURE" }
```

> **Logique interne (backend) :**
> ```typescript
> if (event.type === "payment_intent.succeeded") {
>   const { metadata } = event.data.object;
>   if (metadata.type === "subscription") {
>     // MAJ users : isPremium: true, role: "premium", premiumExpiry (J+30 ou J+365)
>   } else if (metadata.type === "purchase") {
>     // Crée document dans purchases : { userId, contentId, stripePaymentId, amount, purchasedAt }
>   }
> }
> ```

---

## 👤 Écran : Profil Utilisateur

---

### 1. Voir son profil

- **Description :** Retourne les informations complètes du profil de l'utilisateur connecté, avec ses statistiques d'utilisation.
- **Requête :** `GET /user/profile`
- **Accès :** JWT requis

```typescript
// Réponse 200
interface UserProfileResponse {
  _id: string;
  username: string;
  email: string;
  role: UserRole;
  isPremium: boolean;
  premiumExpiry: string | null; // ISO 8601
  createdAt: string;            // ISO 8601
  stats: {
    totalWatched: number;         // nombre de contenus vus/écoutés
    totalPurchases: number;       // nombre d'achats unitaires
    tutorialsInProgress: number;  // tutoriels avec 0 < percentComplete < 100
  };
}
```

---

### 2. Modifier le profil

- **Description :** Met à jour le nom d'utilisateur.
- **Requête :** `PATCH /user/profile`
- **Accès :** JWT requis

```typescript
// Body
interface UpdateProfileDTO {
  username: string; // 3–30 caractères, alphanumérique
}

// Réponse 200
interface UpdateProfileResponse {
  _id: string;
  username: string;
  email: string;
}

// Erreurs
// 400 → { message: "Nom d'utilisateur invalide", code: "INVALID_USERNAME" }
// 409 → { message: "Nom d'utilisateur déjà pris", code: "USERNAME_DUPLICATE" }
```

---

### 3. Changer le mot de passe

- **Description :** Vérifie l'ancien mot de passe avant de le remplacer. Le nouveau est haché avec bcrypt (coût 12).
- **Requête :** `PATCH /user/password`
- **Accès :** JWT requis

```typescript
// Body
interface ChangePasswordDTO {
  currentPassword: string;
  newPassword: string; // minimum 8 caractères
}

// Réponse 200
interface ChangePasswordResponse {
  message: string; // "Mot de passe mis à jour avec succès"
}

// Erreurs
// 401 → { message: "Mot de passe actuel incorrect", code: "WRONG_PASSWORD" }
// 400 → { message: "Nouveau mot de passe trop faible", code: "WEAK_PASSWORD" }
```

---

## 📤 Écran : Espace Fournisseur

Accessible aux utilisateurs avec le rôle `"provider"`. La vignette est **obligatoire** pour tout upload.

---

### 1. Déposer un nouveau contenu

- **Description :** Upload multipart d'un contenu avec vignette obligatoire. Après upload vidéo, `ffmpeg` découpe automatiquement en segments HLS. Le contenu est créé avec `isPublished: false` jusqu'à validation admin.
- **Requête :** `POST /provider/contents`
- **Accès :** JWT + rôle `provider`
- **Content-Type :** `multipart/form-data`

```typescript
// Champs multipart
interface UploadContentDTO {
  thumbnail: File;       // JPEG ou PNG, ≤ 5 Mo — OBLIGATOIRE
  media: File;           // MP4 (vidéo) ou MP3/AAC (audio) — OBLIGATOIRE
  title: string;         // 3–100 caractères
  description: string;   // max 1000 caractères
  type: ContentType;
  category: ContentCategory;
  language: Language;
  accessType: AccessType;
  price?: number;        // requis si accessType === "paid", en centimes
  isTutorial?: boolean;  // défaut : false
}

// Réponse 201
interface UploadContentResponse {
  _id: string;
  title: string;
  thumbnail: string;    // chemin vers /uploads/thumbnails/<uuid>.jpg
  isPublished: boolean; // toujours false à la soumission
  message: string;      // "Votre contenu a été soumis. Il sera visible après validation."
}

// Erreurs
// 400 → { message: "La vignette est obligatoire.", code: "THUMBNAIL_REQUIRED" }
// 400 → { message: "Type MIME non autorisé (JPEG ou PNG uniquement)", code: "INVALID_MIME_TYPE" }
// 400 → { message: "Fichier image trop volumineux (max 5 Mo)", code: "FILE_TOO_LARGE" }
// 400 → { message: "Le prix est requis pour un contenu payant", code: "PRICE_REQUIRED" }
```

---

### 2. Lister ses contenus

- **Description :** Retourne uniquement les contenus appartenant au fournisseur connecté (publiés et en attente).
- **Requête :** `GET /provider/contents`
- **Accès :** JWT + rôle `provider`

```typescript
// Un item fournisseur
interface ProviderContentItem {
  _id: string;
  title: string;
  thumbnail: string;    // jamais null
  accessType: AccessType;
  isPublished: boolean;
  viewCount: number;
  createdAt: string;    // ISO 8601
}

// Réponse 200
interface ProviderContentsResponse {
  contents: ProviderContentItem[];
  total: number;
}
```

---

### 3. Modifier les métadonnées d'un contenu

- **Description :** Met à jour le titre, la description, la catégorie et la langue. Toute modification soumet le contenu à revalidation admin.
- **Requête :** `PUT /provider/contents/:id`
- **Accès :** JWT + rôle `provider` + propriétaire du contenu

```typescript
// Body
interface UpdateContentMetadataDTO {
  title?: string;
  description?: string;
  category?: ContentCategory;
  language?: Language;
}

// Réponse 200
interface UpdateContentMetadataResponse {
  _id: string;
  title: string;
  isPublished: boolean; // repassé à false après modification
  message: string;      // "Modifications soumises. Revalidation admin requise."
}

// Erreurs
// 403 → { message: "Vous n'êtes pas propriétaire de ce contenu", code: "FORBIDDEN" }
```

---

### 4. Remplacer la vignette

- **Description :** Remplace la vignette d'un contenu existant. L'ancienne est supprimée du serveur.
- **Requête :** `PUT /provider/contents/:id/thumbnail`
- **Accès :** JWT + rôle `provider` + propriétaire
- **Content-Type :** `multipart/form-data`

```typescript
// Champs multipart
interface ReplaceThumbnailDTO {
  thumbnail: File; // JPEG ou PNG, ≤ 5 Mo — OBLIGATOIRE
}

// Réponse 200
interface ReplaceThumbnailResponse {
  thumbnail: string; // nouveau chemin : /uploads/thumbnails/<uuid>.jpg
}

// Erreurs
// 400 → { message: "La vignette est obligatoire.", code: "THUMBNAIL_REQUIRED" }
// 403 → { message: "Vous n'êtes pas propriétaire de ce contenu", code: "FORBIDDEN" }
```

---

### 5. Modifier le niveau d'accès et le prix

- **Description :** Change le niveau d'accès et/ou le prix. Soumet à revalidation admin.
- **Requête :** `PUT /provider/contents/:id/access`
- **Accès :** JWT + rôle `provider` + propriétaire

```typescript
// Body
interface UpdateAccessDTO {
  accessType: AccessType;
  price?: number; // requis si accessType === "paid", en centimes
}

// Réponse 200
interface UpdateAccessResponse {
  accessType: AccessType;
  price: number | null;
  isPublished: boolean; // repassé à false
  message: string;      // "Niveau d'accès modifié. Revalidation admin requise."
}

// Erreurs
// 400 → { message: "Le prix est requis pour un contenu payant", code: "PRICE_REQUIRED" }
// 403 → { message: "Vous n'êtes pas propriétaire de ce contenu", code: "FORBIDDEN" }
```

---

### 6. Gérer les leçons d'un tutoriel

- **Description :** Réorganise l'ordre des leçons (glisser-déposer côté frontend), ajoute ou supprime des leçons.
- **Requête :** `PUT /provider/contents/:id/lessons`
- **Accès :** JWT + rôle `provider` + propriétaire

```typescript
// Une leçon dans la requête
interface LessonDTO {
  index: number;    // ordre de la leçon (base 0)
  title: string;
  mediaId: string;  // _id du fichier média associé
}

// Body
interface UpdateLessonsDTO {
  lessons: LessonDTO[];
}

// Réponse 200
interface UpdateLessonsResponse {
  totalLessons: number;
  lessons: LessonDTO[];
}
```

---

### 7. Supprimer un contenu

- **Description :** Supprime le contenu et tous les fichiers associés (vignette, segments HLS, audio).
- **Requête :** `DELETE /provider/contents/:id`
- **Accès :** JWT + rôle `provider` + propriétaire

```typescript
// Body — aucun

// Réponse 200
interface DeleteContentResponse {
  message: string; // "Contenu supprimé avec succès"
}

// Erreurs
// 403 → { message: "Vous n'êtes pas propriétaire de ce contenu", code: "FORBIDDEN" }
```

---

## 🛠️ Écran : Administration

Accessible uniquement aux utilisateurs avec le rôle `"admin"`.

---

### 1. Lister tous les contenus (publiés et en attente)

- **Description :** Vue complète du catalogue incluant les contenus non publiés en attente de validation.
- **Requête :** `GET /admin/contents`
- **Accès :** JWT + rôle `admin`

```typescript
// Query params
interface AdminContentsQueryParams {
  isPublished?: boolean;
  page?: number;
  limit?: number;
}

// Un item admin
interface AdminContentItem {
  _id: string;
  title: string;
  thumbnail: string;
  isPublished: boolean;
  provider: {
    _id: string;
    username: string;
  };
  createdAt: string; // ISO 8601
}

// Réponse 200
interface AdminContentsResponse {
  contents: AdminContentItem[];
  total: number;
}
```

---

### 2. Approuver / Rejeter un contenu

- **Description :** Publie ou rejette un contenu soumis. En cas de rejet, le commentaire est obligatoire.
- **Requête :** `PUT /admin/contents/:id`
- **Accès :** JWT + rôle `admin`

```typescript
// Body — Approbation
interface ApproveContentDTO {
  isPublished: true;
}

// Body — Rejet
interface RejectContentDTO {
  isPublished: false;
  rejectionReason: string; // obligatoire si isPublished === false
}

type AdminUpdateContentDTO = ApproveContentDTO | RejectContentDTO;

// Réponse 200
interface AdminUpdateContentResponse {
  _id: string;
  isPublished: boolean;
  message: string;
}
```

---

### 3. Supprimer un contenu (admin)

- **Description :** Suppression administrative sans restriction de propriété.
- **Requête :** `DELETE /admin/contents/:id`
- **Accès :** JWT + rôle `admin`

```typescript
// Body — aucun

// Réponse 200
interface AdminDeleteResponse {
  message: string; // "Contenu supprimé par l'administrateur"
}
```

---

### 4. Statistiques globales

- **Description :** Tableau de bord administrateur avec métriques de la plateforme et revenus simulés.
- **Requête :** `GET /admin/stats`
- **Accès :** JWT + rôle `admin`

```typescript
// Un contenu top ventes
interface TopContent {
  title: string;
  thumbnail: string;
  totalSales: number;
  totalRevenue: number; // en centimes
}

// Réponse 200
interface AdminStatsResponse {
  totalUsers: number;
  premiumUsers: number;
  totalContents: number;
  publishedContents: number;
  pendingContents: number;
  totalViews: number;
  recentPurchases30d: number;
  revenueSimulated30d: number;       // en centimes
  topPurchasedContents: TopContent[];
}
```

---

### 5. Gestion des utilisateurs

- **Description :** Liste tous les utilisateurs de la plateforme.
- **Requête :** `GET /admin/users`
- **Accès :** JWT + rôle `admin`

```typescript
// Query params
interface AdminUsersQueryParams {
  role?: UserRole;
  page?: number;
  limit?: number; // défaut : 50
}

// Un utilisateur admin
interface AdminUserItem {
  _id: string;
  username: string;
  email: string;
  role: UserRole;
  isPremium: boolean;
  isActive: boolean;
  createdAt: string; // ISO 8601
}

// Réponse 200
interface AdminUsersResponse {
  users: AdminUserItem[];
  total: number;
}
```

---

### 6. Activer / Désactiver un utilisateur

- **Description :** Suspend ou réactive un compte. Un utilisateur désactivé reçoit `401` à chaque tentative de connexion.
- **Requête :** `PUT /admin/users/:id`
- **Accès :** JWT + rôle `admin`

```typescript
// Body
interface ToggleUserDTO {
  isActive: boolean;
}

// Réponse 200
interface ToggleUserResponse {
  _id: string;
  isActive: boolean;
  message: string;
}
```

---

## 🔁 Intercepteur Axios — Gestion Cross-Platform des Erreurs

Ce code est **identique sur web et mobile**. Il gère le renouvellement automatique du JWT (401) et l'affichage des écrans intermédiaires d'accès (403).

```typescript
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Renouvellement JWT automatique
    if (error.response?.status === 401) {
      try {
        const { data }: { data: RefreshResponseWeb | RefreshResponseMobile } =
          await axiosInstance.post("/auth/refresh");

        tokenStore.setToken(data.token);
        error.config.headers["Authorization"] = `Bearer ${data.token}`;
        return axiosInstance.request(error.config);
      } catch {
        tokenStore.logout();
        navigate("/login"); // Web : react-router / Mobile : expo-router
      }
    }

    // Affichage de l'écran intermédiaire d'accès
    if (error.response?.status === 403) {
      const { reason, price }: AccessDeniedError = error.response.data;
      // reason : "subscription_required" | "purchase_required" | "login_required"
      accessGateStore.show({ reason, price });
    }

    return Promise.reject(error);
  }
);
```

---

## 🗺️ Résumé des Routes

| Méthode | Route | Accès | Écran |
|---|---|---|---|
| `POST` | `/auth/register` | Public | Inscription |
| `POST` | `/auth/login` | Public | Connexion |
| `POST` | `/auth/refresh` | Refresh token | Session |
| `POST` | `/auth/logout` | JWT | Session |
| `GET` | `/contents` | Public | Catalogue |
| `GET` | `/contents/featured` | Public | Catalogue |
| `GET` | `/contents/trending` | Public | Catalogue |
| `GET` | `/contents/:id` | Public | Détail contenu |
| `POST` | `/contents/:id/view` | Public | Lecteur |
| `GET` | `/contents/:id/lessons` | JWT + checkAccess | Tutoriels |
| `GET` | `/hls/:id/token` | JWT + checkAccess | Lecteur vidéo |
| `GET` | `/hls/:id/index.m3u8` | Token HLS | Lecteur vidéo |
| `GET` | `/hls/:id/:segment` | Token HLS + fingerprint | Lecteur vidéo |
| `GET` | `/audio/:id/url` | JWT + checkAccess | Lecteur audio |
| `POST` | `/download/:id` | JWT + checkAccess | Hors-ligne (mobile) |
| `POST` | `/history/:contentId` | JWT | Historique |
| `GET` | `/history` | JWT | Historique |
| `POST` | `/tutorial/progress/:id` | JWT | Tutoriels |
| `GET` | `/tutorial/progress` | JWT | Tutoriels |
| `GET` | `/user/profile` | JWT | Profil |
| `PATCH` | `/user/profile` | JWT | Profil |
| `PATCH` | `/user/password` | JWT | Profil |
| `POST` | `/payment/subscribe` | JWT | Abonnement |
| `GET` | `/payment/status` | JWT | Abonnement |
| `POST` | `/payment/purchase` | JWT | Achat unitaire |
| `GET` | `/payment/purchases` | JWT | Profil / Achats |
| `POST` | `/payment/webhook` | Signature Stripe | Interne |
| `POST` | `/provider/contents` | JWT + provider | Espace fournisseur |
| `GET` | `/provider/contents` | JWT + provider | Espace fournisseur |
| `PUT` | `/provider/contents/:id` | JWT + provider + owner | Espace fournisseur |
| `PUT` | `/provider/contents/:id/thumbnail` | JWT + provider + owner | Espace fournisseur |
| `PUT` | `/provider/contents/:id/access` | JWT + provider + owner | Espace fournisseur |
| `PUT` | `/provider/contents/:id/lessons` | JWT + provider + owner | Espace fournisseur |
| `DELETE` | `/provider/contents/:id` | JWT + provider + owner | Espace fournisseur |
| `GET` | `/admin/contents` | JWT + admin | Administration |
| `PUT` | `/admin/contents/:id` | JWT + admin | Administration |
| `DELETE` | `/admin/contents/:id` | JWT + admin | Administration |
| `GET` | `/admin/stats` | JWT + admin | Administration |
| `GET` | `/admin/users` | JWT + admin | Administration |
| `PUT` | `/admin/users/:id` | JWT + admin | Administration |

---

*Documentation générée pour le projet StreamMG — Licence 3 Génie Logiciel — Février 2026*
