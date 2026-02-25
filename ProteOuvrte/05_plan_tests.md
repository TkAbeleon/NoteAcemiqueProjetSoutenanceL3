# Plan de Tests Fonctionnels — StreamMG

**Document :** Plan de tests et rapport de validation  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 1.0  
**Date :** Fevrier 2026  
**Responsable :** Membre 2 — Ingenieur Donnees et Tests

---

## 1. Objectifs et perimetre des tests

Le plan de tests a pour objectif de valider que chaque fonctionnalite declaree dans le cahier des charges se comporte conformement aux specifications, dans les conditions nominales comme dans les cas limites et d'erreur. Les tests sont realises manuellement, avec l'appui de la collection Postman pour les tests d'API backend, et de tests manuels sur navigateur et sur application mobile Expo Go pour les tests d'interface.

Les tests automatises (tests unitaires avec Jest, tests d'integration) sont documentes comme perspectives d'amelioration future et ne sont pas requis dans le cadre de ce projet academique de niveau Licence.

---

## 2. Environnements de test

Les tests sont realises dans deux environnements distincts. L'environnement de developpement local utilise Node.js v20 en local, MongoDB Community Server en local, Expo en mode developpement (expo start), et la CLI Stripe pour la simulation des webhooks (stripe listen). L'environnement de staging, utilise pour la validation pre-soutenance, est identique a l'environnement de production : backend deploye sur Railway, base de donnees sur MongoDB Atlas, frontend web sur Vercel, webhooks Stripe configures dans le tableau de bord Stripe test.

---

## 3. Cas de tests par module

### 3.1 Module Authentification

**TF-AUTH-01 — Inscription avec donnees valides**  
Pre-condition : L'API est demarree. La base de donnees est vide ou ne contient pas l'email de test.  
Entrees : `{ "username": "testuser", "email": "test@streamMG.mg", "password": "Password1" }`  
Requete : POST /api/auth/register  
Resultat attendu : Code HTTP 201. Reponse JSON contenant `{ "message": "Inscription reussie", "user": { "id": "...", "username": "testuser" } }`. Un document est cree dans la collection users avec le mot de passe hache (non en clair).  
Verification post-test : Requete MongoDB `db.users.findOne({ email: "test@streamMG.mg" })` pour confirmer que le champ passwordHash commence par `$2b$` (prefixe bcrypt).

**TF-AUTH-02 — Inscription avec email deja utilise**  
Pre-condition : L'utilisateur TF-AUTH-01 existe en base de donnees.  
Entrees : Meme email que TF-AUTH-01.  
Resultat attendu : Code HTTP 409 Conflict. Message d'erreur "Cette adresse email est deja utilisee".

**TF-AUTH-03 — Connexion avec identifiants valides**  
Pre-condition : L'utilisateur TF-AUTH-01 existe.  
Entrees : `{ "email": "test@streamMG.mg", "password": "Password1" }`  
Requete : POST /api/auth/login  
Resultat attendu : Code HTTP 200. Reponse JSON contenant un champ `accessToken` (JWT). Cookie httpOnly `refreshToken` present dans les en-tetes de reponse Set-Cookie.

**TF-AUTH-04 — Connexion avec mot de passe incorrect**  
Entrees : Email valide, mot de passe incorrect.  
Resultat attendu : Code HTTP 401. Message generique "Identifiants incorrects" (sans preciser quel champ est errone).

**TF-AUTH-05 — Renouvellement automatique du JWT**  
Pre-condition : L'utilisateur TF-AUTH-03 est connecte. Le JWT a expire (simuler en reduisant temporairement la duree de vie a 5 secondes dans les variables d'environnement).  
Action : Envoyer une requete a une route protegee avec le JWT expire. L'intercepteur axios doit detecter le 401, appeler POST /api/auth/refresh avec le refresh token en cookie, obtenir un nouveau JWT, et rejouer la requete initiale.  
Resultat attendu : La requete initiale reussit apres le renouvellement transparent du JWT, sans intervention de l'utilisateur.

**TF-AUTH-06 — Deconnexion**  
Requete : POST /api/auth/logout avec un JWT valide.  
Resultat attendu : Code HTTP 200. Le refresh token est supprime de la base de donnees. Une requete subsequente a POST /api/auth/refresh avec l'ancien cookie retourne 401.

---

### 3.2 Module Catalogue

**TF-CAT-01 — Liste des contenus sans filtre**  
Requete : GET /api/contents  
Resultat attendu : Code HTTP 200. Tableau JSON de contenus pagines (20 elements maximum). Chaque element contient au minimum : _id, title, type, category, duration, thumbnail, viewCount.

**TF-CAT-02 — Filtrage par type audio**  
Requete : GET /api/contents?type=audio  
Resultat attendu : Tous les elements retournes ont le champ `type` egal a "audio".

**TF-CAT-03 — Recherche textuelle**  
Pre-condition : Un contenu avec le titre "Salegy Malagasy" existe en base de donnees.  
Requete : GET /api/contents?search=salegy  
Resultat attendu : Le contenu "Salegy Malagasy" apparait dans les resultats. La recherche est insensible a la casse.

**TF-CAT-04 — Pagination**  
Pre-condition : Plus de 20 contenus existent en base de donnees.  
Requete : GET /api/contents?page=2  
Resultat attendu : La deuxieme page de 20 contenus est retournee. Les contenus de la page 1 ne sont pas repetes.

---

### 3.3 Module Lecture et Historique

**TF-READ-01 — Enregistrement de la progression de lecture**  
Pre-condition : L'utilisateur est connecte. Un contenu audio existe avec l'id `contentId`.  
Requete : POST /api/history/:contentId avec le body `{ "progressSeconds": 127 }`  
Resultat attendu : Code HTTP 200 ou 201. Un document est cree ou mis a jour dans la collection watchHistory avec userId, contentId et progressSeconds = 127.

**TF-READ-02 — Reprise de lecture**  
Pre-condition : TF-READ-01 a ete execute.  
Requete : GET /api/history  
Resultat attendu : La reponse inclut le contenu avec progressSeconds = 127.

**TF-READ-03 — Incrementation du compteur de vues**  
Requete : POST /api/contents/:id/view (route declenchee au demarrage de la lecture)  
Resultat attendu : Le champ viewCount du contenu est incremente de 1 en base de donnees. L'operation est atomique (utilisation de $inc MongoDB).

---

### 3.4 Module Paiement Simule

**TF-PAY-01 — Creation d'un PaymentIntent en mode test**  
Pre-condition : L'utilisateur est connecte. Les cles Stripe test sont configurees.  
Requete : POST /api/payment/create-intent avec `{ "plan": "premium_monthly" }`  
Resultat attendu : Code HTTP 200. Reponse JSON contenant un champ `clientSecret` dont la valeur commence par "pi_" (identifiant de PaymentIntent Stripe).

**TF-PAY-02 — Paiement reussi avec carte de test**  
Action : Soumettre le formulaire Stripe Elements avec la carte 4242 4242 4242 4242, date 12/28, CVV 123.  
Resultat attendu : Stripe retourne un statut "succeeded". Le webhook Stripe declenche la mise a jour de isPremium = true pour l'utilisateur en base de donnees. L'interface affiche l'ecran de confirmation.

**TF-PAY-03 — Paiement refuse avec carte de test**  
Action : Soumettre le formulaire avec la carte 4000 0000 0000 9995.  
Resultat attendu : Stripe retourne un statut "declined". L'interface affiche le message "Votre carte a ete refusee". Le statut isPremium de l'utilisateur reste false en base de donnees.

**TF-PAY-04 — Verification du statut Premium apres souscription**  
Pre-condition : TF-PAY-02 a ete execute avec succes.  
Requete : GET /api/payment/status avec le JWT de l'utilisateur.  
Resultat attendu : Reponse JSON `{ "isPremium": true, "premiumExpiry": "..." }`.

---

### 3.5 Module Administration

**TF-ADMIN-01 — Upload d'un fichier audio**  
Pre-condition : L'utilisateur connecte a le role admin. Un fichier MP3 de test est disponible.  
Requete : POST /api/admin/contents (multipart/form-data avec le fichier MP3 et les metadonnees).  
Resultat attendu : Code HTTP 201. Reponse JSON avec l'ID du nouveau contenu. Un document est cree dans la collection contents. Les metadonnees ID3 (titre, artiste, duree) ont ete extraites automatiquement et correspondent aux metadonnees embarquees dans le fichier MP3.

**TF-ADMIN-02 — Upload refuse pour un non-administrateur**  
Pre-condition : L'utilisateur connecte a le role "user" (non admin).  
Requete : POST /api/admin/contents  
Resultat attendu : Code HTTP 403 Forbidden.

**TF-ADMIN-03 — Consultation des statistiques**  
Pre-condition : Des entrees existent dans la collection watchHistory.  
Requete : GET /api/admin/stats avec le JWT d'un administrateur.  
Resultat attendu : Reponse JSON contenant les tableaux top10Weekly, top10Monthly, totalUsers et activeUsers7d, tous non nuls.

---

### 3.6 Mode hors-ligne (PWA Web)

**TF-OFFLINE-01 — Mise en cache d'un titre audio**  
Pre-condition : L'application web est ouverte dans Chrome. Le Service Worker est actif (verifiable dans Chrome DevTools > Application > Service Workers). Un titre audio est disponible dans le catalogue.  
Action : Cliquer sur l'icone de mise en cache hors-ligne d'un titre audio.  
Resultat attendu : Le fichier audio apparait dans Chrome DevTools > Application > Cache Storage sous la cle "streamMG-offline-audio-v1". L'icone du titre passe a l'etat "disponible hors-ligne".

**TF-OFFLINE-02 — Lecture hors-ligne**  
Pre-condition : TF-OFFLINE-01 a ete execute. La connexion reseau est coupee (mode avion ou DevTools > Network > Offline).  
Action : Naviguer vers le titre audio mis en cache et lancer la lecture.  
Resultat attendu : La lecture demarre normalement, sans erreur reseau, en utilisant le fichier depuis le cache du navigateur.

**TF-OFFLINE-03 — Expiration du cache**  
Pre-condition : Un titre a ete mis en cache. Le Service Worker est configure avec une expiration de 48 heures.  
Action : Simuler l'ecoulement de 48 heures en modifiant l'horodatage stocke dans le cache (via la console DevTools) ou en reduisant le delai d'expiration a 1 minute pour le test.  
Resultat attendu : Le Service Worker supprime le fichier expire du cache. L'icone du titre repasse a l'etat "non mis en cache".

---

## 4. Tests de securite basiques

**TF-SEC-01 — Acces a une route protegee sans JWT**  
Requete : GET /api/history sans en-tete Authorization.  
Resultat attendu : Code HTTP 401 Unauthorized.

**TF-SEC-02 — Acces a une route admin avec un token utilisateur standard**  
Requete : POST /api/admin/contents avec le JWT d'un utilisateur de role "user".  
Resultat attendu : Code HTTP 403 Forbidden.

**TF-SEC-03 — Rate limiting sur la route de connexion**  
Action : Envoyer 6 requetes consecutives a POST /api/auth/login avec des identifiants incorrects depuis la meme IP dans une fenetre de 15 minutes.  
Resultat attendu : La sixieme requete (et les suivantes) recoit une reponse 429 Too Many Requests.

**TF-SEC-04 — Injection dans le champ de recherche**  
Action : Envoyer GET /api/contents?search={"$gt":""} (tentative d'injection NoSQL).  
Resultat attendu : La requete ne retourne pas l'ensemble de la base de donnees. Elle est traitee comme une recherche textuelle sans syntaxe speciale, retournant 0 resultats ou les resultats correspondant a la chaine litterale.

---

## 5. Matrice de traçabilite

La matrice de traçabilite met en correspondance chaque fonctionnalite du cahier des charges avec les cas de test associes, afin de s'assurer qu'aucune specification n'est laissee sans verification.

| Fonctionnalite (CDC) | Cas de test | Statut |
|---|---|---|
| Inscription utilisateur | TF-AUTH-01, TF-AUTH-02 | A valider |
| Connexion utilisateur | TF-AUTH-03, TF-AUTH-04 | A valider |
| Renouvellement JWT | TF-AUTH-05 | A valider |
| Deconnexion | TF-AUTH-06 | A valider |
| Catalogue et filtres | TF-CAT-01 a TF-CAT-04 | A valider |
| Historique de lecture | TF-READ-01, TF-READ-02 | A valider |
| Compteur de vues | TF-READ-03 | A valider |
| Paiement simule (succes) | TF-PAY-01, TF-PAY-02 | A valider |
| Paiement simule (echec) | TF-PAY-03 | A valider |
| Statut Premium | TF-PAY-04 | A valider |
| Upload admin (audio) | TF-ADMIN-01 | A valider |
| Protection routes admin | TF-ADMIN-02 | A valider |
| Statistiques admin | TF-ADMIN-03 | A valider |
| Mode hors-ligne | TF-OFFLINE-01, TF-OFFLINE-02, TF-OFFLINE-03 | A valider |
| Rate limiting | TF-SEC-03 | A valider |
| Protection injection NoSQL | TF-SEC-04 | A valider |

---

## 6. References bibliographiques

Myers, G. J., Sandler, C., & Badgett, T. (2011). *The Art of Software Testing* (3e ed.). Wiley. ISBN 978-1118031964.

Cohn, M. (2004). *User Stories Applied: For Agile Software Development*. Addison-Wesley Professional. ISBN 978-0321205681.

Postman Inc. (2025). *Postman Documentation — Writing Tests*. https://learning.postman.com/docs/writing-scripts/test-scripts

OWASP Foundation. (2021). *OWASP Web Security Testing Guide (WSTG) v4.2*. https://owasp.org/www-project-web-security-testing-guide/

Stripe Inc. (2026). *Testing Stripe.js*. https://stripe.com/docs/testing
