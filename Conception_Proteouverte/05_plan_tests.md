# Plan de Tests Fonctionnels — StreamMG

**Document :** Plan de tests  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026  
**Responsable tests API :** Membre 3  
**Responsable tests mobile :** Membre 1  
**Responsable tests web :** Membre 2

---

## 1. Objectifs et périmètre

Ce plan de tests couvre l'ensemble du système StreamMG, organisé en trois niveaux : tests de l'API backend via Postman (Membre 3), tests de l'interface mobile sur appareil physique et émulateur (Membre 1), et tests de l'interface web sur navigateurs (Membre 2). Une attention particulière est portée au middleware checkAccess, aux achats unitaires, et à la progression des tutoriels, qui constituent les fonctionnalités nouvelles et critiques du système.

---

## 2. Tests authentification — API (Membre 3)

**TF-AUTH-01 — Inscription valide.**
POST /api/auth/register `{ username, email, password }`. Résultat attendu : 201, document utilisateur créé en base avec passwordHash (jamais le mot de passe en clair), rôle "user", isPremium false.

**TF-AUTH-02 — Inscription email dupliqué.**
POST /api/auth/register avec un email déjà existant. Résultat attendu : 409 "Email déjà utilisé".

**TF-AUTH-03 — Connexion valide.**
POST /api/auth/login. Résultat attendu : 200, JWT dans le corps, refresh token en cookie httpOnly.

**TF-AUTH-04 — Renouvellement JWT.**
POST /api/auth/refresh avec un refresh token valide. Résultat attendu : nouveau JWT, nouveau refresh token (rotation), ancien token invalidé en base.

**TF-AUTH-05 — Déconnexion.**
POST /api/auth/logout. Résultat attendu : 200, document refresh token supprimé de la collection refreshTokens.

---

## 3. Tests du middleware checkAccess — API (Membre 3)

Ces tests sont les plus critiques du projet. Une erreur dans checkAccess pourrait exposer des contenus protégés ou bloquer des accès légitimes.

**TF-ACC-01 — Contenu gratuit accessible sans JWT.**
GET /api/contents/:id/stream sans header Authorization, contenu accessType: "free". Résultat attendu : 200 et accès au fichier.

**TF-ACC-02 — Contenu premium refusé à un utilisateur standard.**
GET /api/contents/:id/stream avec JWT rôle "user", contenu accessType: "premium". Résultat attendu : 403 `{ reason: "subscription_required" }`.

**TF-ACC-03 — Contenu premium accessible à un utilisateur premium.**
Même requête avec JWT rôle "premium". Résultat attendu : 200 et accès au fichier.

**TF-ACC-04 — Contenu payant refusé sans achat (utilisateur standard).**
GET /api/contents/:id/stream avec JWT rôle "user", contenu accessType: "paid", aucun achat dans purchases. Résultat attendu : 403 `{ reason: "purchase_required", price: 500000 }`.

**TF-ACC-05 — Contenu payant accessible après achat.**
Même requête après insertion d'un document dans purchases pour cet utilisateur et ce contenu. Résultat attendu : 200 et accès au fichier.

**TF-ACC-06 — Contenu payant refusé à un utilisateur PREMIUM sans achat.**
GET /api/contents/:id/stream avec JWT rôle "premium", contenu accessType: "paid", aucun achat. Résultat attendu : 403 `{ reason: "purchase_required" }`. Ce test vérifie que l'abonnement Premium ne couvre pas les contenus payants.

**TF-ACC-07 — Administrateur accède à tout contenu.**
GET /api/contents/:id/stream avec JWT rôle "admin", contenu accessType: "paid" non acheté. Résultat attendu : 200. L'admin n'est jamais bloqué.

---

## 4. Tests catalogue — API (Membre 3)

**TF-CAT-01 — Liste paginée.**
GET /api/contents?page=1&limit=20. Résultat attendu : 200, tableau de contenus avec pagination.

**TF-CAT-02 — Filtre par niveau d'accès.**
GET /api/contents?accessType=free. Résultat attendu : uniquement des contenus avec accessType "free".

**TF-CAT-03 — Filtre tutoriels.**
GET /api/contents?isTutorial=true. Résultat attendu : uniquement des contenus avec isTutorial true.

**TF-CAT-04 — Recherche textuelle.**
GET /api/contents?search=salegy. Résultat attendu : contenus dont le titre ou l'artiste contient "salegy".

**TF-CAT-05 — Incrémentation vues.**
POST /api/contents/:id/view. Résultat attendu : viewCount incrémenté de 1 (opération $inc atomique MongoDB).

---

## 5. Tests achats unitaires — API (Membre 3)

**TF-PUR-01 — Création d'un PaymentIntent d'achat.**
POST /api/payment/purchase `{ contentId }` avec JWT valide, utilisateur sans achat antérieur. Résultat attendu : 200, champ clientSecret dans la réponse. Vérifier dans le tableau de bord Stripe test que le PaymentIntent contient `metadata.type === "purchase"`, userId et contentId.

**TF-PUR-02 — Achat réussi et création du document purchases.**
Compléter le PaymentIntent avec la carte 4242 4242 4242 4242 (via CLI Stripe ou formulaire frontend). Résultat attendu : webhook reçu → document créé dans purchases avec userId, contentId, stripePaymentId, amount, purchasedAt → GET /api/contents/:id/stream retourne 200 pour cet utilisateur.

**TF-PUR-03 — Idempotence : tentative de double achat.**
POST /api/payment/purchase avec le même contentId pour un utilisateur ayant déjà un achat. Résultat attendu : 409 "Vous avez déjà acheté ce contenu". Aucun PaymentIntent Stripe créé. Aucun document inséré.

**TF-PUR-04 — Achat avec carte de refus.**
Initier un achat, soumettre la carte 4000 0000 0000 9995. Résultat attendu : Stripe retourne un échec → aucun webhook → aucun document dans purchases → accès toujours refusé.

**TF-PUR-05 — Liste des achats de l'utilisateur.**
GET /api/payment/purchases. Résultat attendu : tableau contenant les contenus achetés avec titre, description et vignette (populate Mongoose).

---

## 6. Tests progression tutoriels — API (Membre 3)

**TF-TUT-01 — Enregistrement de la progression.**
POST /api/tutorial/progress/:tutorialId `{ lessonIndex: 0, completed: true }`. Résultat attendu : document tutorialProgress créé avec completedLessons: [0], percentComplete calculé.

**TF-TUT-02 — Avancement progressif.**
Après TF-TUT-01, POST avec `{ lessonIndex: 1, completed: true }`. Résultat attendu : document mis à jour, completedLessons: [0, 1], percentComplete recalculé, lastUpdatedAt mis à jour.

**TF-TUT-03 — Tutoriel marqué comme terminé.**
POST avec la dernière leçon d'un tutoriel de 3 leçons. Résultat attendu : percentComplete: 100.

**TF-TUT-04 — Récupération des tutoriels en cours.**
GET /api/tutorial/progress. Résultat attendu : tableau de tous les tutoriels commencés avec percentComplete < 100, ordonnés par lastUpdatedAt décroissant.

---

## 7. Tests sécurité — API (Membre 3)

**TF-SEC-01 — Accès sans JWT sur route protégée.**
GET /api/provider/contents sans header Authorization. Résultat attendu : 401.

**TF-SEC-02 — Accès route admin avec token utilisateur.**
GET /api/admin/stats avec JWT rôle "user". Résultat attendu : 403.

**TF-SEC-03 — Rate limiting authentification.**
11 requêtes POST /api/auth/login en moins de 15 minutes depuis la même IP. Résultat attendu : la 11ème requête retourne 429 Too Many Requests.

**TF-SEC-04 — Fournisseur ne peut pas modifier le contenu d'un autre.**
PUT /api/provider/contents/:id avec JWT d'un fournisseur différent du uploadedBy du contenu. Résultat attendu : 403.

**TF-SEC-05 — Webhook Stripe avec signature invalide.**
POST /api/payment/webhook avec un body valide mais une signature Stripe incorrecte. Résultat attendu : 400, aucune modification en base.

---

## 8. Tests interface mobile (Membre 1)

**TF-MOB-01 — Badges de niveau d'accès dans le catalogue.**
Parcourir le catalogue sur l'application mobile. Résultat attendu : contenus gratuits sans badge, contenus premium avec badge or "★ Premium", contenus payants avec badge teal et prix en ariary.

**TF-MOB-02 — Écran intermédiaire premium.**
Utilisateur standard clique sur un contenu premium. Résultat attendu : écran "Abonnez-vous à Premium" avec bouton de redirection vers la page d'abonnement.

**TF-MOB-03 — Écran intermédiaire payant.**
Utilisateur (standard ou premium) clique sur un contenu payant non acheté. Résultat attendu : écran d'achat avec le prix correct du contenu et bouton "Acheter".

**TF-MOB-04 — Lecture vidéo en mode paysage.**
Lancer la lecture d'une vidéo. Résultat attendu : passage automatique en mode paysage via expo-screen-orientation, contrôles fonctionnels, retour portrait à la fermeture.

**TF-MOB-05 — Mini-player persistant.**
Lancer une lecture audio, naviguer vers une autre page. Résultat attendu : le mini-player reste visible au-dessus de la tab bar, la lecture continue sans interruption.

**TF-MOB-06 — Mode hors-ligne audio.**
Télécharger un fichier audio via expo-file-system, désactiver le réseau (mode avion). Résultat attendu : le fichier audio se lit depuis le chemin local, sans erreur réseau.

**TF-MOB-07 — Flux d'achat Stripe mobile.**
Initier un achat sur un contenu payant, saisir 4242 4242 4242 4242 dans le CardField natif. Résultat attendu : confirmation d'achat, bouton "Lire" actif, accès débloqué.

**TF-MOB-08 — Session persistante au redémarrage.**
Fermer complètement l'application, la rouvrir. Résultat attendu : l'utilisateur est reconnecté automatiquement (renouvellement silencieux du JWT via refresh token depuis expo-secure-store).

**TF-MOB-09 — Progression tutoriel.**
Terminer une leçon d'un tutoriel. Résultat attendu : barre de progression mise à jour, pourcentage affiché sur la carte du tutoriel, leçon suivante proposée.

---

## 9. Tests interface web (Membre 2)

**TF-WEB-01 — Badges de niveau d'accès.**
Même test que TF-MOB-01 sur Chrome, Firefox et Safari.

**TF-WEB-02 — Écrans intermédiaires.**
Mêmes tests que TF-MOB-02 et TF-MOB-03 sur le web.

**TF-WEB-03 — Mini-player persistant.**
Lancer une lecture audio, naviguer via react-router-dom vers une autre page. Résultat attendu : mini-player toujours présent, lecture non interrompue.

**TF-WEB-04 — Cache audio Service Worker (mode hors-ligne).**
Lire un titre audio, ouvrir DevTools → Application → Cache Storage → vérifier que le fichier est en cache. Désactiver le réseau via DevTools. Relire le titre. Résultat attendu : lecture depuis le cache, sans requête réseau.

**TF-WEB-05 — Expiration du cache 48h.**
Simuler un horodatage de cache dépassé de 48h (manipulation du timestamp en cache). Résultat attendu : le Service Worker refuse la version en cache et tente une requête réseau.

**TF-WEB-06 — Flux d'achat Stripe Web.**
Initier un achat, saisir 4242 4242 4242 4242 dans Stripe Elements (iframe). Résultat attendu : confirmation, accès débloqué.

**TF-WEB-07 — Responsivité 360px.**
Redimensionner le navigateur à 360px de largeur. Résultat attendu : interface lisible, boutons cliquables, texte non tronqué, grille adaptée.

**TF-WEB-08 — Progression tutoriel.**
Même test que TF-MOB-09 sur le web.

---

## 10. Matrice de traçabilité

| Fonctionnalité (CDC) | Cas de test | Responsable |
|---|---|---|
| Contenu gratuit accessible à tous | TF-ACC-01 | M3 |
| Premium refusé sans abonnement | TF-ACC-02 | M3 |
| Premium accessible avec abonnement | TF-ACC-03 | M3 |
| Payant refusé sans achat | TF-ACC-04, TF-ACC-06 | M3 |
| Payant accessible après achat | TF-ACC-05 | M3 |
| Admin accède à tout | TF-ACC-07 | M3 |
| PaymentIntent achat unitaire | TF-PUR-01 | M3 |
| Achat réussi + document purchases | TF-PUR-02 | M3 |
| Idempotence double achat | TF-PUR-03 | M3 |
| Achat refusé (carte invalide) | TF-PUR-04 | M3 |
| Liste achats utilisateur | TF-PUR-05 | M3 |
| Progression tutoriel (enreg.) | TF-TUT-01 à TF-TUT-03 | M3 |
| Tutoriels en cours (liste) | TF-TUT-04 | M3 |
| Sécurité JWT + roles | TF-SEC-01 à TF-SEC-05 | M3 |
| Badges niveaux — mobile | TF-MOB-01 | M1 |
| Écrans intermédiaires — mobile | TF-MOB-02, TF-MOB-03 | M1 |
| Vidéo paysage | TF-MOB-04 | M1 |
| Mini-player persistant — mobile | TF-MOB-05 | M1 |
| Hors-ligne expo-file-system | TF-MOB-06 | M1 |
| Achat Stripe — mobile | TF-MOB-07 | M1 |
| Session persistante | TF-MOB-08 | M1 |
| Progression tutoriel — mobile | TF-MOB-09 | M1 |
| Badges niveaux — web | TF-WEB-01 | M2 |
| Écrans intermédiaires — web | TF-WEB-02 | M2 |
| Mini-player persistant — web | TF-WEB-03 | M2 |
| Cache Service Worker | TF-WEB-04, TF-WEB-05 | M2 |
| Achat Stripe — web | TF-WEB-06 | M2 |
| Responsivité 360px | TF-WEB-07 | M2 |
| Progression tutoriel — web | TF-WEB-08 | M2 |

---

## 11. Références bibliographiques

Myers, G. J., Sandler, C., & Badgett, T. (2011). *The Art of Software Testing* (3e éd.). Wiley. ISBN 978-1118031964.

Postman Inc. (2025). *Postman Documentation*. https://learning.postman.com/docs

OWASP Foundation. (2021). *OWASP Web Security Testing Guide v4.2*. https://owasp.org/www-project-web-security-testing-guide/

Stripe Inc. (2026). *Testing Stripe integrations*. https://stripe.com/docs/testing
