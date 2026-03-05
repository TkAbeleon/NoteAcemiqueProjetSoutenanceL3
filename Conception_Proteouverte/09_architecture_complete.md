# Contrat d'API et Architecture Complète — StreamMG

**Document :** Contrat d'API REST — référence de coordination inter-membres  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026  
**Producteur :** Membre 3 — Backend  
**Consommateurs :** Membre 1 (mobile), Membre 2 (web)

---

## 1. Principes généraux de l'API

L'API REST de StreamMG est la source unique de vérité partagée entre les trois membres. Toute modification de signature d'endpoint, de format de réponse ou de code d'erreur doit être communiquée aux trois membres simultanément.

**Base URL :** `https://api.streamMG.railway.app/api` (production) — `http://localhost:3001/api` (développement local)

**Format :** JSON exclusivement pour le corps des requêtes et des réponses.

**Authentification :** JWT Bearer Token dans le header `Authorization: Bearer <token>`. Les routes marquées "JWT" exigent ce header. Les routes marquées "Public" sont accessibles sans token.

**Refresh token :** Transmis via cookie httpOnly sur le web (navigateur le gère automatiquement) ou via expo-secure-store sur mobile (inclus manuellement dans les requêtes de renouvellement).

**Erreurs standard :**

| Code | Signification |
|---|---|
| 400 | Données invalides (validation express-validator) |
| 401 | Token absent, expiré ou invalide |
| 403 | Accès refusé (rôle insuffisant ou contenu protégé) |
| 404 | Ressource introuvable |
| 409 | Conflit (email déjà utilisé, achat déjà effectué) |
| 429 | Rate limit dépassé |
| 500 | Erreur serveur interne |

**Format de réponse 403 du middleware checkAccess :**
```json
{
  "reason": "subscription_required" | "purchase_required" | "login_required",
  "price": 800000  // Présent uniquement si reason === "purchase_required"
}
```

---

## 2. Authentification

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /auth/register | Public | Inscription |
| POST | /auth/login | Public | Connexion |
| POST | /auth/refresh | Cookie/SecureStore | Renouvellement JWT |
| POST | /auth/logout | JWT | Déconnexion |

**POST /auth/register**
```json
// Requête
{ "username": "Rabe", "email": "rabe@exemple.mg", "password": "MotDePasse1" }

// Réponse 201
{ "token": "eyJhb...", "user": { "_id": "...", "username": "Rabe", "role": "user", "isPremium": false } }
```

**POST /auth/login**
```json
// Requête
{ "email": "rabe@exemple.mg", "password": "MotDePasse1" }

// Réponse 200 + cookie httpOnly "refreshToken"
{ "token": "eyJhb...", "user": { "_id": "...", "username": "Rabe", "role": "user", "isPremium": true } }
```

**POST /auth/refresh**
```json
// Réponse 200
{ "token": "eyJhb..." }
// Erreur si refresh token expiré ou révoqué
{ "message": "Session expirée, veuillez vous reconnecter" }  // 401
```

---

## 3. Catalogue

| Méthode | Route | Accès | Description |
|---|---|---|---|
| GET | /contents | Public | Liste paginée avec filtres |
| GET | /contents/featured | Public | Contenus mis en avant |
| GET | /contents/trending | Public | Top 10 de la semaine |
| GET | /contents/:id | Public | Détail d'un contenu |
| POST | /contents/:id/view | Public | Incrémenter le compteur de vues |
| GET | /contents/:id/stream | JWT + checkAccess | Accès au fichier média |
| GET | /contents/:id/lessons | JWT + checkAccess | Leçons d'un tutoriel |

**GET /contents — paramètres de filtre**
```
?page=1&limit=20          — Pagination (défaut : page 1, 20 résultats)
?type=video|audio         — Filtre par type
?category=film|salegy|... — Filtre par catégorie
?accessType=free|premium|paid — Filtre par niveau d'accès
?isTutorial=true|false    — Filtre tutoriels
?search=salegy            — Recherche textuelle (titre, artiste)
```

**GET /contents — réponse**
```json
{
  "contents": [
    {
      "_id": "...",
      "title": "Mora Mora",
      "type": "audio",
      "category": "salegy",
      "thumbnail": "/uploads/thumbnails/mora_mora.jpg",
      "duration": 243,
      "accessType": "premium",
      "price": null,
      "isTutorial": false,
      "artist": "Tarika Sammy",
      "viewCount": 1842
    }
  ],
  "total": 148,
  "page": 1,
  "pages": 8
}
```

**GET /contents/:id/lessons — réponse (tutoriel accessible)**
```json
{
  "lessons": [
    { "order": 1, "title": "Introduction", "duration": 480, "filePath": "/uploads/video/lecon1.mp4" },
    { "order": 2, "title": "Les rythmes de base", "duration": 720, "filePath": "/uploads/video/lecon2.mp4" }
  ],
  "totalLessons": 8
}
```

---

## 4. Historique et progression

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /history/:contentId | JWT | Enregistrer la progression |
| GET | /history | JWT | Historique de l'utilisateur |
| POST | /tutorial/progress/:contentId | JWT | Mise à jour progression tutoriel |
| GET | /tutorial/progress | JWT | Tutoriels en cours |

**POST /history/:contentId**
```json
// Requête (envoyé toutes les 10 secondes en lecture)
{ "progressSeconds": 342 }
// Réponse 200
{ "message": "Progression enregistrée" }
```

**GET /history — réponse**
```json
{
  "history": [
    {
      "_id": "...",
      "contentId": { "_id": "...", "title": "Ambiaty", "thumbnail": "...", "duration": 5820 },
      "progressSeconds": 1240,
      "isCompleted": false,
      "lastWatchedAt": "2026-02-20T19:30:00.000Z"
    }
  ]
}
```

**POST /tutorial/progress/:contentId**
```json
// Requête
{ "lessonIndex": 2, "completed": true }
// Réponse 200
{
  "lastLessonIndex": 2,
  "completedLessons": [0, 1, 2],
  "percentComplete": 37.5
}
```

**GET /tutorial/progress — réponse**
```json
{
  "inProgress": [
    {
      "contentId": { "_id": "...", "title": "Apprendre le salegy", "thumbnail": "..." },
      "lastLessonIndex": 2,
      "percentComplete": 37.5,
      "lastUpdatedAt": "2026-02-20T20:15:00.000Z"
    }
  ]
}
```

---

## 5. Paiement

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /payment/subscribe | JWT | Abonnement Premium |
| POST | /payment/purchase | JWT | Achat unitaire |
| GET | /payment/purchases | JWT | Liste des achats |
| GET | /payment/status | JWT | Statut Premium de l'utilisateur |
| POST | /payment/webhook | Signature Stripe | Réception événements Stripe |

**POST /payment/subscribe**
```json
// Requête
{ "plan": "monthly" }  // ou "yearly"
// Réponse 200
{ "clientSecret": "pi_3Oq...secret_..." }
```

**POST /payment/purchase**
```json
// Requête
{ "contentId": "65f3a2b4c8e9d1234567890d" }
// Réponse 200
{ "clientSecret": "pi_3Oq...secret_..." }
// Réponse 409 — doublon
{ "message": "Vous avez déjà acheté ce contenu" }
```

**GET /payment/purchases — réponse**
```json
{
  "purchases": [
    {
      "_id": "...",
      "contentId": {
        "_id": "...", "title": "Ny Fitiavana", "thumbnail": "...", "type": "video"
      },
      "amount": 800000,
      "purchasedAt": "2026-02-15T16:22:10.000Z"
    }
  ]
}
```

**POST /payment/webhook — logique de traitement**
```javascript
// Le handler distingue les deux types d'événements via metadata.type
if (event.type === 'payment_intent.succeeded') {
  const metadata = event.data.object.metadata;

  if (metadata.type === 'subscription') {
    // Mettre à jour users : isPremium: true, role: "premium", premiumExpiry
    // Créer un document dans transactions

  } else if (metadata.type === 'purchase') {
    // Créer un document dans purchases :
    // { userId: metadata.userId, contentId: metadata.contentId,
    //   stripePaymentId: event.data.object.id, amount, purchasedAt: now }
  }
}
```

---

## 6. Espace fournisseur

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /provider/contents | JWT + provider | Upload d'un contenu (multipart) |
| GET | /provider/contents | JWT + provider | Ses contenus uniquement |
| PUT | /provider/contents/:id | JWT + provider + owner | Modifier les métadonnées |
| PUT | /provider/contents/:id/access | JWT + provider + owner | Modifier niveau d'accès et prix |
| PUT | /provider/contents/:id/lessons | JWT + provider + owner | Réorganiser les leçons |
| DELETE | /provider/contents/:id | JWT + provider + owner | Supprimer |

**PUT /provider/contents/:id/access**
```json
// Requête
{ "accessType": "paid", "price": 750000 }
// Réponse 200
{ "message": "Niveau d'accès modifié. En attente de validation administrateur.",
  "isPublished": false }
// Note : toute modification de niveau d'accès repasse isPublished à false
```

**PUT /provider/contents/:id/lessons**
```json
// Requête — tableau complet des leçons dans leur nouvel ordre
{
  "lessons": [
    { "order": 1, "title": "Introduction", "filePath": "/uploads/video/lecon1.mp4", "duration": 480 },
    { "order": 2, "title": "Les bases", "filePath": "/uploads/video/lecon2.mp4", "duration": 720 }
  ]
}
```

---

## 7. Administration

| Méthode | Route | Accès | Description |
|---|---|---|---|
| GET | /admin/contents | JWT + admin | Tous les contenus (publiés et non publiés) |
| PUT | /admin/contents/:id | JWT + admin | Modifier y compris isPublished |
| DELETE | /admin/contents/:id | JWT + admin | Supprimer |
| GET | /admin/stats | JWT + admin | Statistiques globales + revenus simulés |
| GET | /admin/users | JWT + admin | Liste des utilisateurs |
| PUT | /admin/users/:id | JWT + admin | Activer / désactiver un compte |

**GET /admin/stats — réponse**
```json
{
  "totalUsers": 284,
  "premiumUsers": 47,
  "totalContents": 312,
  "totalViews": 18420,
  "topPurchasedContents": [
    { "title": "Ny Fitiavana", "totalSales": 12, "totalRevenue": 9600000 }
  ],
  "recentPurchases30d": 38,
  "revenueSimulated30d": 28500000
}
```

---

## 8. Logique frontend — gestion des erreurs 403

Les deux frontends (mobile et web) implémentent la logique suivante dans un intercepteur axios centralisé, pour éviter la duplication dans chaque composant :

```javascript
// axios.interceptor.js — partagé entre mobile et web
axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Tentative de renouvellement du JWT
      try {
        const { data } = await axiosInstance.post('/auth/refresh');
        tokenStore.setToken(data.token);
        error.config.headers['Authorization'] = `Bearer ${data.token}`;
        return axiosInstance.request(error.config);
      } catch {
        tokenStore.logout();
        navigate('/login');
      }
    }

    if (error.response?.status === 403) {
      const { reason, price } = error.response.data;
      // Déclencher l'affichage de l'écran intermédiaire approprié
      accessGateStore.show({ reason, price });
    }

    return Promise.reject(error);
  }
);
```

---

## 9. Références bibliographiques

Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures* (Thèse de doctorat). University of California, Irvine. https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm

Stripe Inc. (2026). *Stripe API Reference — PaymentIntents*. https://stripe.com/docs/api/payment_intents

Stripe Inc. (2026). *Webhooks — Best practices*. https://stripe.com/docs/webhooks/best-practices

TanStack. (2025). *TanStack Query v5*. https://tanstack.com/query/latest

OWASP Foundation. (2023). *OWASP Top Ten 2023*. https://owasp.org/www-project-top-ten/

Martin, R. C. (2017). *Clean Architecture*. Prentice Hall. ISBN 978-0134494166.
