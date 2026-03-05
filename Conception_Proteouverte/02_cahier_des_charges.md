# Cahier des Charges — StreamMG

**Document :** Cahier des Charges Fonctionnel et Technique  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026  
**Rédigé par :** Équipe StreamMG  
**Niveau :** Licence 3 Génie Logiciel

---

## Table des matières

1. Présentation générale du projet
2. Contexte et problématique
3. Acteurs du système
4. Modèle économique et niveaux d'accès
5. Description fonctionnelle par module
6. Architecture technique
7. Base de données
8. Sécurité
9. Design et interfaces
10. Contraintes et exigences non fonctionnelles
11. Repartition des rôles
12. Planning prévisionnel
13. Livrables attendus
14. Références bibliographiques

---

## 1. Présentation générale du projet

### 1.1 Identification du projet

StreamMG est une plateforme numérique de streaming audiovisuel et éducatif dédiée aux contenus culturels et pédagogiques malgaches. Elle permet la diffusion de films, de musique traditionnelle (salegy, hira gasy, tsapiky, beko), de documentaires, de podcasts et de tutoriels organisés en séries de leçons.

La plateforme se compose de trois composants techniques distincts et indépendants, développés par une équipe de trois membres spécialisés.

**Application mobile** (Membre 1) : développée avec React Native et Expo SDK 52, elle cible les smartphones iOS et Android. La démonstration s'effectue via Expo Go.

**Application web** (Membre 2) : développée avec React.js 18 et Vite 5, elle fonctionne dans tout navigateur moderne (Chrome, Firefox, Safari, Edge) et est installable comme Progressive Web App (PWA).

**API REST backend** (Membre 3) : développée avec Node.js 20 LTS et Express.js 4, elle constitue le seul point de vérité partagé entre les deux applications frontend. Elle gère l'authentification, le catalogue, les paiements, la sécurité et toute la logique métier.

### 1.2 Périmètre du projet

StreamMG est un projet académique de groupe, mené en parallèle des mémoires de licence individuels de chaque membre. Le périmètre est délibérément délimité pour garantir la livraison d'un prototype fonctionnel et démontrable en soutenance, sans sacrifier la qualité technique et la cohérence architecturale.

---

## 2. Contexte et problématique

### 2.1 Situation culturelle et numérique à Madagascar

Madagascar possède un patrimoine audiovisuel et musical d'une richesse exceptionnelle : le hira gasy (théâtre musical traditionnel des hautes terres), le salegy (musique populaire du nord), le tsapiky (rythmes du sud-ouest), le beko, les documentaires sur la biodiversité unique de l'île, les productions cinématographiques locales et les émissions culturelles radiophoniques. Ce patrimoine reste pourtant absent, ou quasi absent, des grandes plateformes internationales de diffusion numérique. Netflix, Spotify, Amazon Prime Video ou YouTube Premium proposent des catalogues massivement orientés vers les productions occidentales. Les rares contenus africains ou malgaches qui y figurent représentent une fraction marginale de l'offre, inaccessible de surcroît pour une majorité de la population en raison du coût des abonnements.

### 2.2 Contexte numérique malgache

Selon DataReportal (2025), Madagascar compte environ 18,2 millions de connexions mobiles actives (56,2 % de la population), mais seulement 6,6 millions d'internautes (20,4 %). Le mobile est donc le premier et souvent le seul terminal numérique accessible. La bande passante est inégale : connexion 4G disponible en zones urbaines mais coûteuse, 3G ou 2G en zones rurales. Ces contraintes d'infrastructure justifient plusieurs décisions d'architecture : le mode hors-ligne, l'adaptation au débit, et le choix d'un dark mode par défaut qui consomme moins de batterie sur les écrans OLED.

### 2.3 Problématique adressée

Le besoin adressé par StreamMG est double. D'un côté, les créateurs et producteurs de contenus culturels et éducatifs malgaches disposent de peu de canaux de diffusion numérique structurés. De l'autre, les utilisateurs finaux n'ont pas accès à une plateforme centralisant les contenus de leur culture, adaptée à leurs contraintes financières et de connectivité.

StreamMG répond à ces deux besoins par un modèle économique freemium multi-niveaux : les contenus gratuits assurent l'accessibilité au plus grand nombre, les contenus premium et payants permettent aux fournisseurs de valoriser leur travail, et les tutoriels apportent une dimension éducative distinctive.

---

## 3. Acteurs du système

Le système distingue cinq types d'acteurs, chacun avec des droits et des restrictions précisément définis.

### 3.1 Visiteur

Toute personne accédant à la plateforme (mobile ou web) sans être authentifiée. Il peut consulter le catalogue en entier — titres, descriptions, vignettes — et lire uniquement les contenus de niveau "gratuit". Pour tout autre contenu, il voit un écran d'invitation à s'inscrire. Il ne bénéficie pas du suivi de progression ni de l'historique de lecture.

### 3.2 Utilisateur standard

Personne inscrite et connectée avec un compte gratuit (rôle "user"). Il peut lire tous les contenus gratuits, y compris les tutoriels gratuits avec suivi de progression, créer des playlists personnelles, consulter son historique de lecture, écouter des contenus audio en mode hors-ligne (mobile via téléchargement local, web via Service Worker PWA), et acheter des contenus payants à l'unité via Stripe en mode test.

### 3.3 Utilisateur premium

Personne disposant d'un abonnement Premium actif (rôle "premium"). Il bénéficie de tous les droits de l'utilisateur standard, plus l'accès illimité à l'ensemble des contenus de niveau "premium" : films, albums musicaux complets, documentaires, tutoriels premium. Pour les contenus de niveau "payant", il doit également procéder à un achat unitaire — l'abonnement Premium ne couvre jamais les contenus payants.

### 3.4 Fournisseur de contenu

Producteur ou détenteur de droits culturels malgaches disposant d'un compte de rôle "provider" (label musical, réalisateur, association culturelle, formateur). Il peut uploader des contenus, définir leur niveau d'accès (gratuit, premium ou payant) et fixer leur prix si payant, organiser ses tutoriels en séries de leçons ordonnées, gérer et dépublier ses propres contenus uniquement. Il ne peut en aucun cas accéder aux contenus des autres fournisseurs, aux statistiques globales de la plateforme, ni aux comptes utilisateurs. Toutes ses soumissions sont validées par un administrateur avant publication dans le catalogue.

### 3.5 Administrateur

Membre de l'équipe disposant d'un accès complet. Il valide ou rejette les soumissions des fournisseurs, modifie le niveau d'accès ou le prix de n'importe quel contenu, consulte les statistiques globales d'utilisation et de revenus simulés, et gère les comptes utilisateurs (activation, désactivation).

---

## 4. Modèle économique et niveaux d'accès

### 4.1 Principe général

StreamMG adopte un modèle freemium multi-niveaux. Ce modèle, inspiré de plateformes comme Spotify ou YouTube Premium, combine une offre gratuite accessible au plus grand nombre avec des offres monétisées qui garantissent la viabilité économique de la plateforme et rémunèrent les fournisseurs de contenu. Il est particulièrement adapté au contexte malgache, où le pouvoir d'achat est variable et où l'accessibilité culturelle est un objectif explicite.

### 4.2 Les quatre niveaux d'accès

**Niveau 1 — Contenu gratuit.** Accessible à tous, y compris aux visiteurs non inscrits, sans aucune restriction. C'est le fournisseur qui décide de rendre un contenu gratuit lors de l'upload, généralement pour accroître sa visibilité. Les contenus gratuits constituent la vitrine de la plateforme.

**Niveau 2 — Contenu premium.** Accessible exclusivement aux abonnés Premium. L'abonnement donne accès à l'ensemble du catalogue premium de manière illimitée pendant la durée de l'abonnement : films malgaches, albums musicaux complets, documentaires, tutoriels premium. Ce modèle est identique à celui de Netflix : un forfait mensuel ou annuel donne accès à un catalogue entier.

**Niveau 3 — Contenu payant (achat unitaire).** Accessible après un achat unitaire permanent, indépendant de tout abonnement. Que l'utilisateur soit standard ou Premium, il doit payer ce contenu séparément. Une fois acheté, l'accès est permanent et définitif, même en cas de désabonnement. Ce niveau est conçu pour des contenus à forte valeur ajoutée : un film en avant-première, une master class d'un artiste reconnu, un événement exceptionnel.

**Niveau 4 — Tutoriel.** Les tutoriels suivent exactement le même système d'accès (gratuit, premium ou payant), mais avec une logique fonctionnelle supplémentaire : ils sont organisés en séries de leçons ordonnées, et la plateforme enregistre la progression de chaque utilisateur.

### 4.3 Tableau synthétique des droits d'accès

| Type de contenu | Visiteur | Standard | Premium | Remarque |
|---|---|---|---|---|
| Gratuit | OUI | OUI | OUI | Sans restriction |
| Premium | NON | NON | OUI | Abonnement requis |
| Payant (achat unitaire) | NON | ACHAT | ACHAT | Indépendant de l'abonnement |
| Tutoriel gratuit | OUI | OUI | OUI | + progression trackée |
| Tutoriel premium | NON | NON | OUI | + progression trackée |
| Tutoriel payant | NON | ACHAT | ACHAT | + progression trackée |

**Point important :** un utilisateur Premium qui tente d'accéder à un contenu payant reçoit le même écran d'achat qu'un utilisateur standard. L'abonnement Premium ne constitue jamais un passe-droit pour les contenus de niveau "payant". Cette règle est appliquée côté backend par le middleware `checkAccess`, indépendamment du rôle contenu dans le JWT.

### 4.4 Qui définit le niveau d'accès

C'est le fournisseur de contenu qui, lors de l'upload, définit le niveau d'accès de son contenu et le prix unitaire pour les contenus payants. Cette décision est soumise à la validation de l'administrateur avant publication. Le fournisseur peut modifier ce niveau après publication (sous réserve de revalidation par l'administrateur).

### 4.5 Simulation des paiements

Tous les paiements — abonnement Premium et achats unitaires — sont simulés via Stripe en mode test. Aucune transaction financière réelle n'a lieu. Les prix sont fictifs et exprimés en ariary malgache symbolique. Stripe fournit des numéros de carte de test pour toutes les démonstrations : la carte 4242 4242 4242 4242 simule un paiement accepté, la carte 4000 0000 0000 9995 simule un refus.

---

## 5. Description fonctionnelle par module

### 5.1 Module Authentification

L'inscription requiert un nom d'utilisateur unique (3 à 30 caractères), une adresse email valide, et un mot de passe d'au moins 8 caractères comportant au moins une majuscule et un chiffre. La validation est effectuée en temps réel côté client avant toute soumission, afin de réduire les allers-retours réseau. Le backend valide à nouveau les données, vérifie l'unicité de l'email et du nom d'utilisateur, hache le mot de passe avec bcrypt (facteur de coût 12), crée le document utilisateur en base avec le rôle "user" et isPremium à false.

La connexion génère un JWT d'une durée de validité de 15 minutes et un refresh token de 7 jours. Le JWT est stocké en mémoire vive (variable zustand, pas dans localStorage ni AsyncStorage) pour se prémunir contre les attaques XSS. Le refresh token est stocké de manière sécurisée : cookie httpOnly sur le web (géré automatiquement par le navigateur), expo-secure-store sur mobile (chiffrement natif via iOS Keychain et Android Keystore). Le renouvellement du JWT est automatique et transparent : un intercepteur axios détecte les erreurs 401, appelle POST /api/auth/refresh, et rejoue la requête initiale sans intervention de l'utilisateur.

### 5.2 Module Catalogue

La page d'accueil présente une sélection mise en avant (héro), les tendances de la semaine, les derniers ajouts, et les catégories disponibles. La navigation par catégorie couvre : films malgaches, séries télévisées, musique traditionnelle (hira gasy, salegy, tsapiky, beko), musique contemporaine, documentaires, podcasts et émissions culturelles, et tutoriels.

Pour chaque contenu, un indicateur visuel signale son niveau d'accès : aucun badge pour les contenus gratuits, un badge or "★ Premium" pour les contenus premium, un badge teal avec le prix en ariary pour les contenus payants. La recherche est textuelle, porte sur les titres et les artistes, et est insensible à la casse. Le filtrage par catégorie et par type (vidéo ou audio) est disponible.

Lors d'une tentative de lecture d'un contenu protégé, l'API retourne une erreur 403 avec un champ `reason`. Le frontend affiche l'écran intermédiaire adapté : invitation à s'abonner si `reason === "subscription_required"`, ou invitation à acheter avec le prix affiché si `reason === "purchase_required"`. Ces écrans sont conçus pour être bienveillants et pédagogiques, jamais punitifs.

### 5.3 Module Lecture

**Sur mobile**, la lecture vidéo est assurée par expo-av avec passage automatique en mode paysage via expo-screen-orientation. La lecture audio utilise également expo-av avec un mini-player persistant positionné au-dessus de la tab bar.

**Sur web**, la lecture vidéo et audio est assurée par react-player qui s'appuie sur l'élément HTML5 natif. Le mini-player audio persistant est rendu dans App.tsx en dehors du RouterProvider, garantissant qu'il ne se démonte jamais lors des navigations entre pages.

La position de lecture (progression en secondes) est enregistrée toutes les 10 secondes via POST /api/history/:contentId. Lors du retour sur un contenu, la lecture reprend automatiquement à la position mémorisée. Lorsque l'utilisateur atteint 90 % de la durée d'un contenu, celui-ci est marqué comme terminé et disparaît de la section "Continuer à regarder".

### 5.4 Module Tutoriels

Les tutoriels sont des contenus organisés en séries de leçons ordonnées. Chaque leçon est un fichier média (vidéo ou audio) indépendant avec son titre, sa description, sa durée et son ordre dans la série. Exemples concrets de tutoriels : "Apprendre le salegy — 8 leçons vidéo" (accès premium), "Cuisiner le romazava traditionnel — 5 leçons vidéo" (accès gratuit), "Initiation à la programmation en malgache — 15 leçons" (accès payant, prix : 10 000 Ar).

La plateforme enregistre la progression de chaque utilisateur dans chaque tutoriel : dernière leçon consultée (index), liste des leçons terminées (tableau d'indices), pourcentage de complétion calculé, date de début et date de dernière mise à jour. Une section "Mes tutoriels en cours" dans le profil liste les tutoriels commencés avec leur barre de progression. Le bouton "Continuer" sur la carte d'un tutoriel ramène directement à la dernière leçon non terminée.

### 5.5 Module Abonnement Premium

L'utilisateur accède au flux d'abonnement depuis son profil ou depuis un écran intermédiaire d'accès refusé. Il sélectionne un plan : mensuel (fictif : 5 000 Ar/mois) ou annuel (fictif : 50 000 Ar/an). Le frontend envoie POST /api/payment/subscribe avec le plan sélectionné. Le backend crée un PaymentIntent Stripe en mode test et retourne le client_secret. Le formulaire de saisie de carte s'affiche : Stripe Elements (iframe sécurisée) sur web, composant CardField natif de @stripe/stripe-react-native sur mobile. L'utilisateur saisit la carte de test et confirme. Le backend reçoit le webhook Stripe "payment_intent.succeeded", met à jour isPremium à true, le rôle à "premium", et premiumExpiry à J+30 (plan mensuel) ou J+365 (plan annuel). L'utilisateur voit l'écran de confirmation.

### 5.6 Module Achat Unitaire

L'achat unitaire est accessible depuis la page de détail d'un contenu payant via le bouton "Acheter — [prix] Ar". Le frontend envoie POST /api/payment/purchase avec l'identifiant du contenu. Le backend vérifie d'abord qu'aucun achat antérieur n'existe dans la collection purchases pour cette paire (userId, contentId). Si l'achat est un doublon, il retourne 409 "Vous avez déjà acheté ce contenu". Sinon, il crée un PaymentIntent Stripe avec le montant du contenu, en incluant dans les metadata les champs type: "purchase", userId et contentId. Le flux de saisie de carte est identique à celui de l'abonnement. Le backend reçoit le webhook Stripe, distingue les événements d'abonnement des événements d'achat via `metadata.type`, crée un document dans la collection purchases, et débloque immédiatement l'accès. Le bouton "Acheter" est remplacé par "Lire" sur la page de détail.

L'achat est permanent : même en cas de désabonnement ou de suppression du compte Premium, l'accès aux contenus achetés est maintenu.

### 5.7 Module Mode hors-ligne

**Sur web (PWA)**, le Service Worker intercepte les requêtes vers les fichiers audio. Il implémente une stratégie "Cache First" : si le fichier est en cache et non expiré (durée d'expiration : 48 heures), il est servi depuis le cache sans contacter le serveur. L'utilisateur sélectionne les contenus à mettre en cache via une icône dédiée. Les fichiers expirés sont supprimés automatiquement.

**Sur mobile**, expo-file-system permet le téléchargement local des fichiers audio dans le répertoire documentDirectory de l'application (espace de stockage privé et chiffré). L'URL locale est enregistrée dans AsyncStorage. Lors de la lecture hors-ligne, le lecteur charge le fichier local plutôt que de contacter le serveur.

### 5.8 Module Fournisseur de contenu

L'espace fournisseur est accessible via la route /provider sur web et via un onglet dédié sur mobile, après vérification du rôle "provider" dans le JWT. Le formulaire d'upload inclut : titre, description, type (vidéo ou audio), catégorie, sous-catégorie, langue (malgache, français, bilingue), et les métadonnées spécifiques au type (artiste, album, numéro de piste pour l'audio ; réalisateur, distribution, résolution pour la vidéo). Le niveau d'accès est sélectionné dans un menu déroulant (Gratuit, Premium, Payant). Si "Payant" est sélectionné, un champ de saisie du prix en ariary apparaît. Pour les tutoriels, le fournisseur accède à un gestionnaire de séries de leçons permettant d'ajouter, de réordonner et de supprimer des leçons.

Côté backend, Multer traite l'upload du fichier média. music-metadata extrait automatiquement les métadonnées ID3 (titre, artiste, durée, pochette) des fichiers audio. Le document est créé en base avec isPublished: false et uploadedBy correspondant à l'identifiant du fournisseur. Le fournisseur reçoit la confirmation "Votre contenu a été soumis. Il sera visible après validation."

### 5.9 Module Administration

Le tableau de bord administrateur est accessible depuis /admin (web) ou depuis un menu dédié (mobile), après vérification du rôle "admin". Il propose la gestion complète du catalogue (création, modification, suppression, publication de tous les contenus), la validation des soumissions des fournisseurs (aperçu du contenu, approbation ou rejet avec commentaire), la modification du niveau d'accès ou du prix de n'importe quel contenu, les statistiques globales d'utilisation (contenus les plus vus, catégories populaires, activité par période), les statistiques de revenus simulés (achats unitaires par contenu et par fournisseur sur 7 et 30 jours), et la gestion des comptes utilisateurs (activation, désactivation).

---

## 6. Architecture technique

### 6.1 Pattern architectural

L'architecture adopte le pattern multi-client avec backend partagé. Deux clients frontend distincts et indépendants consomment la même API REST, qui constitue le seul contrat partagé entre les trois composants. Ce pattern est représentatif des organisations d'équipes réelles en entreprise et est académiquement défendable comme illustration de la séparation des préoccupations.

```
[App Mobile — React Native/Expo]     [App Web — React.js/Vite]
        Membre 1                              Membre 2
              \                                  /
               ——————[ HTTPS / REST JSON + JWT ]——————
                                  |
                    [API REST — Node.js/Express]
                          Membre 3
                         /         \
                   [MongoDB]   [Stockage /uploads]
                                       |
                             [Stripe API — mode test]
```

L'API est agnostique du client qui la consomme : qu'une requête provienne de l'application mobile ou du navigateur web, elle reçoit le même traitement et retourne la même réponse JSON.

### 6.2 Stack technologique complète

**Application mobile — Membre 1**

| Composant | Technologie | Version |
|---|---|---|
| Framework | React Native | 0.76.x |
| Boîte à outils | Expo SDK | 52 |
| Navigation | expo-router | v3.x |
| Lecture média | expo-av | v14.x |
| Stockage local | expo-file-system | latest |
| Stockage sécurisé | expo-secure-store | latest |
| Paiement | @stripe/stripe-react-native | latest |
| État global | zustand | v4.x |
| Requêtes API | TanStack Query | v5.x |
| Client HTTP | axios | latest |
| Styling | NativeWind | v4.x |

**Application web — Membre 2**

| Composant | Technologie | Version |
|---|---|---|
| Bibliothèque UI | React.js | 18.x |
| Build tool | Vite | 5.x |
| Navigation | react-router-dom | v6.x |
| Lecture média | react-player | v2.x |
| Paiement | @stripe/react-stripe-js | latest |
| PWA / hors-ligne | Service Worker (Workbox) | latest |
| État global | zustand | v4.x |
| Requêtes API | TanStack Query | v5.x |
| Client HTTP | axios | latest |
| Styling | Tailwind CSS | v3.x |

**Backend — Membre 3**

| Composant | Technologie | Version |
|---|---|---|
| Environnement | Node.js LTS | 20.x |
| Framework serveur | Express.js | v4.x |
| ODM | Mongoose | v8.x |
| Authentification | jsonwebtoken | v9.x |
| Hachage | bcryptjs | v2.x |
| Upload fichiers | Multer | v1.x |
| Métadonnées audio | music-metadata | v10.x |
| Paiement | stripe (SDK) | v14.x |
| Sécurité headers | helmet | latest |
| CORS | cors | latest |
| Rate limiting | express-rate-limit | latest |
| Validation | express-validator | latest |

**Infrastructure**

| Composant | Solution |
|---|---|
| Base de données | MongoDB v7.x (Atlas, cluster M0 gratuit) |
| Hébergement backend | Railway |
| Hébergement frontend web | Vercel |
| Démonstration mobile | Expo Go (QR code) |
| Reverse proxy | Nginx avec SSL Let's Encrypt |
| Gestion de version | Git / GitHub (branches par feature) |
| Documentation API | Postman (collection exportée) |
| Maquettes | Figma |

### 6.3 Le contrat d'API

Le contrat d'API est le document de coordination central entre les trois membres. Il est produit par le Membre 3 en début de projet et consommé par les Membres 1 et 2, qui peuvent développer leurs interfaces en parallèle en mockant les réponses pendant la phase initiale.

**Authentification**

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /api/auth/register | Public | Inscription |
| POST | /api/auth/login | Public | Connexion, retourne JWT + cookie refresh |
| POST | /api/auth/refresh | Cookie refresh | Renouvellement du JWT |
| POST | /api/auth/logout | JWT | Déconnexion, suppression du refresh token |

**Catalogue**

| Méthode | Route | Accès | Description |
|---|---|---|---|
| GET | /api/contents | Public | Liste paginée, filtres : type, category, accessType, isTutorial, search |
| GET | /api/contents/:id | Public | Détail d'un contenu |
| GET | /api/contents/featured | Public | Contenus mis en avant |
| GET | /api/contents/trending | Public | Top 10 contenus de la semaine |
| GET | /api/contents/:id/lessons | JWT + checkAccess | Leçons d'un tutoriel |
| POST | /api/contents/:id/view | Public | Incrémentation du compteur de vues |

**Historique et progression**

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /api/history/:contentId | JWT | Enregistrement de la progression (body : progressSeconds) |
| GET | /api/history | JWT | Historique de l'utilisateur avec détails des contenus |
| POST | /api/tutorial/progress/:contentId | JWT | Mise à jour de la progression dans un tutoriel (body : lessonIndex, completed) |
| GET | /api/tutorial/progress | JWT | Tous les tutoriels en cours avec percentComplete |

**Paiement**

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /api/payment/subscribe | JWT | Crée un PaymentIntent d'abonnement, retourne clientSecret |
| POST | /api/payment/purchase | JWT | Crée un PaymentIntent d'achat unitaire après vérification doublon, retourne clientSecret |
| GET | /api/payment/purchases | JWT | Liste des contenus achetés par l'utilisateur |
| GET | /api/payment/status | JWT | Statut Premium (isPremium, premiumExpiry) |
| POST | /api/payment/webhook | Signature Stripe | Réception des événements Stripe (abonnement et achats) |

**Fournisseur**

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | /api/provider/contents | JWT + provider | Upload d'un contenu (multipart) |
| GET | /api/provider/contents | JWT + provider | Ses propres contenus uniquement |
| PUT | /api/provider/contents/:id | JWT + provider + propriétaire | Modification des métadonnées |
| PUT | /api/provider/contents/:id/access | JWT + provider + propriétaire | Modification du niveau d'accès et du prix |
| PUT | /api/provider/contents/:id/lessons | JWT + provider + propriétaire | Réorganisation des leçons |
| DELETE | /api/provider/contents/:id | JWT + provider + propriétaire | Suppression |

**Administration**

| Méthode | Route | Accès | Description |
|---|---|---|---|
| GET | /api/admin/contents | JWT + admin | Tous les contenus avec statut isPublished |
| PUT | /api/admin/contents/:id | JWT + admin | Modification complète incluant isPublished |
| GET | /api/admin/stats | JWT + admin | Statistiques globales + revenus simulés |
| GET | /api/admin/users | JWT + admin | Liste des utilisateurs |
| PUT | /api/admin/users/:id | JWT + admin | Activation / désactivation de compte |

---

## 7. Base de données

### 7.1 Choix de MongoDB

MongoDB (v7.x) est retenu pour sa capacité à gérer la nature hétérogène des métadonnées des contenus audiovisuels. Un film possède des attributs (résolution, sous-titres, réalisateur, distribution) qui n'ont pas de sens pour un titre audio (artiste, album, numéro de piste, pochette). Un tutoriel possède un tableau de leçons imbriquées qui n'existe pas dans les autres types de contenus. Le modèle document JSON de MongoDB accueille cette flexibilité naturellement, sans nécessiter des colonnes nullable ou des tables de jointure complexes.

### 7.2 Collections et schémas

**Collection users**

```
_id          : ObjectId
username     : String, unique, 3-30 caractères
email        : String, unique, format email
passwordHash : String, hachage bcrypt (préfixe $2b$)
role         : String, enum : "user" | "premium" | "provider" | "admin"
isPremium    : Boolean, défaut false
premiumExpiry: Date, null si non premium
avatar       : String, URL optionnelle
isActive     : Boolean, défaut true
createdAt    : Date (Mongoose timestamps)
updatedAt    : Date (Mongoose timestamps)

Index : email (unique), username (unique), role (simple)
```

**Collection contents**

```
_id          : ObjectId
title        : String, obligatoire
description  : String, obligatoire
type         : String, enum : "video" | "audio"
category     : String (film, salegy, hira-gasy, documentaire, podcast, tutoriel...)
subCategory  : String, optionnel
language     : String, enum : "mg" | "fr" | "bilingual"
thumbnail    : String, URL
filePath     : String, chemin du fichier principal (absent si isTutorial)
fileSize     : Number, en octets
mimeType     : String
duration     : Number, en secondes (absent si isTutorial)
viewCount    : Number, défaut 0
isPublished  : Boolean, défaut false
uploadedBy   : ObjectId, référence users._id

-- Niveau d'accès (modèle économique) --
accessType   : String, enum : "free" | "premium" | "paid", défaut "free"
price        : Number, en centimes, null si accessType !== "paid"
              (ex : 800000 pour 8 000 Ar)

-- Tutoriels --
isTutorial   : Boolean, défaut false
lessons      : Array d'objets (présent uniquement si isTutorial === true)
  {
    order       : Number, position dans la série (commence à 1)
    title       : String
    description : String
    filePath    : String, chemin du fichier de la leçon
    duration    : Number, en secondes
  }

-- Champs audio optionnels --
artist, album, coverArt, trackNumber

-- Champs vidéo optionnels --
resolution, subtitles, director, cast

Index : texte composite (title, artist), category, type, accessType,
        viewCount (décroissant), uploadedBy, isPublished, isTutorial
```

**Collection purchases** *(achats unitaires)*

```
_id             : ObjectId
userId          : ObjectId, référence users._id
contentId       : ObjectId, référence contents._id
stripePaymentId : String, identifiant PaymentIntent Stripe ("pi_...")
amount          : Number, montant payé en centimes (conservé pour l'historique)
purchasedAt     : Date, horodatage de la confirmation webhook Stripe

Index : { userId, contentId } UNIQUE — garantit l'idempotence des achats
        stripePaymentId UNIQUE — prévient le traitement double des webhooks
        userId (simple) — pour la requête "mes achats"
```

**Collection tutorialProgress** *(progression dans les tutoriels)*

```
_id              : ObjectId
userId           : ObjectId, référence users._id
contentId        : ObjectId, référence contents._id (le tutoriel)
lastLessonIndex  : Number, index de la dernière leçon consultée
completedLessons : [Number], indices des leçons terminées (≥ 90 % de la durée)
percentComplete  : Number, calculé : completedLessons.length / lessons.length × 100
startedAt        : Date
lastUpdatedAt    : Date

Index : { userId, contentId } UNIQUE — un seul document par paire
        userId (simple) — pour la section "Mes tutoriels en cours"
```

**Collection watchHistory** *(historique de lecture)*

```
_id             : ObjectId
userId          : ObjectId, référence users._id
contentId       : ObjectId, référence contents._id
progressSeconds : Number, position de lecture en secondes
isCompleted     : Boolean, défaut false
lastWatchedAt   : Date

Index : { userId, contentId } UNIQUE, { userId, lastWatchedAt } décroissant
```

**Collection playlists**

```
_id        : ObjectId
userId     : ObjectId
name       : String
contentIds : [ObjectId], liste ordonnée de références
isPublic   : Boolean, défaut false
createdAt, updatedAt : Date

Index : userId (simple)
```

**Collection refreshTokens**

```
_id       : ObjectId
userId    : ObjectId
tokenHash : String, hachage bcrypt du token (jamais le token en clair)
expiresAt : Date, J+7 depuis la création

Index : tokenHash (unique), expiresAt (TTL, expireAfterSeconds: 0),
        userId (simple)
```

**Collection transactions** *(registre des paiements Stripe)*

```
_id             : ObjectId
userId          : ObjectId
stripePaymentId : String
plan            : String, enum : "premium_monthly" | "premium_yearly"
amount          : Number, en centimes
currency        : String, "mga"
status          : String, enum : "pending" | "succeeded" | "failed" | "canceled"
stripeEvent     : Object, copie de l'événement webhook pour audit
createdAt, updatedAt : Date

Index : userId (simple), stripePaymentId (unique), status (simple)
```

---

## 8. Sécurité

### 8.1 Authentification et gestion des tokens

L'authentification repose sur des JWT à courte durée de vie (15 minutes) signés avec une clé secrète HS256 stockée en variable d'environnement (jamais en dur dans le code). Les JWT sont transmis dans le header Authorization : Bearer. Ils sont stockés en mémoire vive uniquement (variable zustand) pour se prémunir contre les attaques XSS : un script malveillant injecté dans la page ne peut pas accéder à localStorage ou sessionStorage.

Le refresh token a une durée de validité de 7 jours et est soumis à une rotation systématique : à chaque renouvellement, l'ancien token est invalidé en base (suppression du document dans refreshTokens) et un nouveau est émis. En cas de vol d'un refresh token, la fenêtre d'exploitation est limitée à la durée entre le vol et le prochain renouvellement. Le hash du refresh token (bcrypt) est stocké en base, jamais le token en clair.

### 8.2 Vérification des droits d'accès — middleware checkAccess

Le middleware `checkAccess` est la pièce centrale du modèle économique côté sécurité. Il est monté sur toutes les routes de streaming et de récupération des leçons. Son algorithme :

1. Charge le contenu depuis MongoDB pour lire son champ `accessType`.
2. Si `accessType === "free"` : accès autorisé pour tous (req.user peut être null).
3. Si `accessType === "premium"` : vérifie que req.user existe et que son rôle est "premium" ou "admin". Sinon, retourne 403 avec `{ reason: "subscription_required" }`.
4. Si `accessType === "paid"` : l'administrateur a toujours accès. Pour tout autre rôle, vérifie l'existence d'un document dans la collection purchases pour la paire (userId, contentId). Sinon, retourne 403 avec `{ reason: "purchase_required", price: content.price }`.
5. Tout champ accessType absent ou invalide : accès refusé par défaut (principe du moindre privilège).

### 8.3 Hachage des mots de passe

bcrypt avec un facteur de coût de 12. Ce facteur implique 2¹² = 4 096 itérations de hachage, rendant les attaques par force brute prohibitivement coûteuses en temps de calcul. Les mots de passe ne sont jamais stockés en clair ni en MD5 ou SHA.

### 8.4 Sécurité des routes

Le middleware `auth.middleware.js` vérifie et décode le JWT sur toutes les routes authentifiées, et injecte les informations de l'utilisateur (id, rôle) dans `req.user`. Le middleware `admin.middleware.js` vérifie que `req.user.role === "admin"`. Le middleware `provider.middleware.js` vérifie que `req.user.role === "provider"` ou `"admin"`. Les routes fournisseur vérifient également que `content.uploadedBy.toString() === req.user.id`, ce qui interdit strictement à un fournisseur de modifier les contenus d'un autre.

### 8.5 Headers de sécurité HTTP

Helmet est configuré avec les directives suivantes : Strict-Transport-Security (force HTTPS, durée 1 an), X-Content-Type-Options: nosniff (prévient le MIME sniffing), X-Frame-Options: DENY (prévient le clickjacking), Content-Security-Policy (contrôle des sources autorisées pour les scripts, styles et médias).

### 8.6 Rate limiting

express-rate-limit est configuré avec des fenêtres strictes sur les routes d'authentification : 10 requêtes par IP par fenêtre de 15 minutes sur /api/auth/login et /api/auth/register (prévention des attaques par credential stuffing). Les autres routes sont limitées à 200 requêtes par IP par 15 minutes.

### 8.7 Validation des entrées et des uploads

express-validator valide toutes les données soumises par les utilisateurs avant tout traitement. Multer est configuré pour n'accepter que les types MIME autorisés (video/mp4, audio/mpeg, audio/aac, image/jpeg, image/png) avec une taille maximale de fichier de 500 Mo pour les vidéos et 50 Mo pour les audios.

### 8.8 Configuration CORS

Le backend autorise uniquement les origines connues : le domaine de production du frontend web (Vercel) et localhost:5173 en développement. Les requêtes sans header Origin (applications mobiles natives, Postman) sont autorisées. L'option credentials: true est nécessaire pour la transmission des cookies httpOnly du refresh token.

---

## 9. Design et interfaces

### 9.1 Direction artistique

Le design system de StreamMG adopte une direction de **raffinement sombre et chaleureux**, inspirée des grandes plateformes de streaming tout en affirmant une identité culturelle malgache. Le dark mode est le mode par défaut — choix fonctionnel adapté aux conditions d'usage malgaches (luminosité variable, économie de batterie sur les écrans OLED). Un light mode est disponible mais non prioritaire dans le MVP.

Les deux applications (mobile et web) partagent les mêmes tokens de design (couleurs, typographie, espacements, rayons de bord), ce qui garantit une cohérence d'expérience entre les plateformes.

### 9.2 Palette de couleurs

| Rôle | Couleur | Hexadécimal | Usage |
|---|---|---|---|
| Principale | Bleu cobalt | #3584e4 | Boutons primaires, liens actifs, indicateurs |
| Principale light | Bleu clair | #62a0ea | Hover, états actifs secondaires |
| Accent or | Or | #e8c547 | Badge Premium, étoiles — utilisé avec parcimonie |
| Accent teal | Teal | #2ec27e | Badge payant, bouton d'achat unitaire |
| Fond base | Bleu-gris très foncé | #0d1018 | Fond de l'application |
| Fond surface | Bleu-gris foncé | #171b26 | Cartes, modales |
| Fond raised | Bleu-gris moyen | #202434 | Éléments surélevés, hover |
| Texte principal | Blanc cassé | #eef0f6 | Titres, contenu principal |
| Texte secondaire | Gris bleuté | #8d96a8 | Descriptions, métadonnées |
| Succès | Vert | #57e389 | Confirmation paiement, leçon terminée |
| Erreur | Rouge | #ed333b | Échec paiement, carte refusée |
| Avertissement | Jaune | #f5c211 | Premium expirant bientôt |

### 9.3 Typographie

Deux familles de polices sont utilisées, disponibles gratuitement sur Google Fonts.

**Sora** (affichage) : police sans-serif géométrique aux terminaisons légèrement arrondies, utilisée pour les titres (h1 à h4), les noms de contenus dans les cartes, et les CTA. Son weight 800 est particulièrement efficace pour les grands titres héros.

**DM Sans** (corps) : police conçue pour les interfaces numériques, avec une excellente lisibilité aux petites tailles. Utilisée pour les descriptions, les métadonnées, les labels de formulaires.

L'échelle typographique suit un ratio de 1.25 (Major Third), produisant des niveaux de 11px à 39px.

### 9.4 Composants principaux

**Carte de contenu (ContentCard)** : vignette en ratio 5:7 (portrait, adapté aux affiches et pochettes), badge de niveau d'accès en superposition en haut à droite, zone de texte avec titre et métadonnées. Sur web, effet de survol avec translation verticale de -5px et halo bleu.

**Badges de niveau** : badge or "★ Premium" pour les contenus premium, badge teal avec le prix en ariary pour les contenus payants. Aucun badge pour les contenus gratuits (absence de badge = gratuit).

**Mini-player audio** : barre de progression interactive (3px), pochette, titre et artiste, contrôles (précédent, lecture/pause, suivant). Persistant sur toutes les pages sur les deux plateformes.

**Écrans intermédiaires** : écran bienveillant (non punitif) s'affichant lors d'un accès refusé. Deux variantes : invitation à l'abonnement (fond bleu translucide, icône étoile or) et invitation à l'achat (fond teal translucide, icône cadenas, prix affiché).

**Barre de navigation web** : topbar sticky de 60px avec logo, liens de navigation, barre de recherche, et bouton Premium. Effet verre dépoli (backdrop-filter: blur) au scroll.

**Tab bar mobile** : barre d'onglets fixée en bas (56px + safe area système) avec 4 onglets : Accueil, Explorer, Recherche, Profil.

### 9.5 Accessibilité

Les contrastes respectent les critères WCAG 2.1 niveau AA. Le rapport de contraste entre le texte principal (#eef0f6) et le fond de base (#0d1018) atteint 16.2:1 (minimum requis : 4.5:1). Tous les éléments interactifs sont navigables au clavier sur le web. Les cibles tactiles respectent la taille minimale de 44×44 points sur mobile.

---

## 10. Contraintes et exigences non fonctionnelles

**Performance.** Le temps de réponse de l'API pour les requêtes de liste et de détail doit être inférieur à 500 ms. Le middleware checkAccess, appelé sur chaque requête de streaming, doit s'exécuter en moins de 100 ms.

**Compatibilité.** L'application mobile doit fonctionner sur iOS 14+ et Android 10+. L'application web doit être compatible avec les dernières versions de Chrome, Firefox, Safari et Edge, et être responsive à partir de 360 pixels de largeur.

**Idempotence des achats.** Si un utilisateur tente d'acheter deux fois le même contenu (double-clic, retour arrière), le système retourne une erreur claire 409 sans créer de double PaymentIntent Stripe ni de double document en base. L'index unique sur {userId, contentId} dans la collection purchases garantit cette propriété au niveau de la base de données.

**Cohérence des tokens.** Le renouvellement du JWT doit être automatique et transparent. L'intercepteur axios doit rejeter correctement les erreurs 401, renouveler le token, et rejouer la requête initiale sans perte de données ni déconnexion non voulue.

**Sécurité des uploads.** Les fichiers médias uploadés par les fournisseurs sont validés en type MIME et en taille avant stockage. Les chemins de fichiers ne sont jamais exposés directement dans les réponses API destinées aux utilisateurs finaux non autorisés.

**Scalabilité.** Bien que le projet soit académique, les index MongoDB sont conçus pour les requêtes réelles de production. L'architecture sans état (stateless) du backend, où chaque requête est authentifiée par son propre JWT, permet une scalabilité horizontale sans partage d'état de session.

---

## 11. Répartition des rôles

| Membre | Domaine | Charge | Responsabilités principales |
|---|---|---|---|
| Membre 1 | Frontend Mobile | 38 % | Intégralité de l'app React Native/Expo : navigation, lecteurs, mini-player, hors-ligne (expo-file-system), écrans de niveau d'accès, flux Stripe mobile, tutoriels avec progression |
| Membre 2 | Frontend Web | 32 % | Intégralité de l'app React.js/Vite : navigation SPA, lecteurs, mini-player, PWA Service Worker, écrans de niveau d'accès, Stripe Elements, tutoriels avec progression, responsivité |
| Membre 3 | Backend + Coordination | 30 % | API REST complète, MongoDB/Mongoose (8 collections), Multer, music-metadata, Stripe SDK, middleware checkAccess, sécurité applicative (JWT, bcrypt, CORS, helmet, rate-limit, validation), Nginx/SSL, contrat d'API, coordination générale |

**Principe de coordination.** Le Membre 3 produit le contrat d'API complet (signatures de tous les endpoints, formats de réponse, codes d'erreur) en semaine 1, avant que les Membres 1 et 2 ne commencent le développement de leurs interfaces. Les Membres 1 et 2 développent en parallèle en utilisant des données mockées pendant les premières semaines, puis s'intègrent avec le vrai backend lorsque les modules fondamentaux sont disponibles.

---

## 12. Planning prévisionnel

| Phase | Semaines | Membre 1 | Membre 2 | Membre 3 |
|---|---|---|---|---|
| Conception | S1–S2 | Init projet Expo, maquettes Figma mobile | Init projet Vite, maquettes Figma web | Contrat d'API complet, schémas MongoDB, init backend |
| Développement — Authentification | S3 | Écrans login/register, zustand authStore | Pages login/register, zustand authStore | Routes auth, JWT, bcrypt, refresh tokens |
| Développement — Catalogue | S4 | Catalogue, recherche, filtres, cartes avec badges | Catalogue, recherche, filtres, cartes avec badges | Routes contents, index MongoDB, upload Multer |
| Développement — Lecture | S5 | Lecteurs expo-av, mini-player, hors-ligne mobile | Lecteurs react-player, mini-player, Service Worker PWA | Routes history, tutorialProgress |
| Développement — Paiement | S6 | Stripe React Native, écrans d'accès (premium/payant) | Stripe Elements, écrans d'accès (premium/payant) | Stripe SDK, webhook, checkAccess, purchases |
| Développement — Admin/Provider | S7 | Interface fournisseur mobile, admin mobile | Interface fournisseur web, admin web | Routes admin/provider, stats, déploiement staging |
| Tests | S8–S9 | Tests interface mobile, correction anomalies | Tests interface web, correction anomalies | Tests API Postman, tests sécurité, correction anomalies |
| Soutenance | S10 | Démonstration mobile, contribution mémoire | Démonstration web, contribution mémoire | Finalisation documentation, préparation démonstration |

---

## 13. Livrables attendus

**Code source.** Trois dépôts GitHub distincts et indépendants : frontend-mobile (React Native/Expo), frontend-web (React.js/Vite), backend (Node.js/Express). Chaque dépôt contient un fichier README.md détaillant les instructions d'installation et de lancement.

**Applications déployées.** Backend déployé sur Railway avec variables d'environnement configurées. Frontend web déployé sur Vercel avec règles de rewrite SPA. Frontend mobile accessible via Expo Go (QR code pointant vers l'API de staging).

**Documentation API.** Collection Postman exportée au format JSON, incluant tous les endpoints documentés avec des exemples de requêtes et de réponses, des variables d'environnement (URL de base, tokens de test), et les tests automatisés Postman pour chaque cas de test fonctionnel.

**Maquettes.** Fichier Figma contenant les maquettes haute fidélité des écrans principaux pour les deux plateformes (mobile et web) : accueil, catalogue, détail d'un contenu, lecteur, profil, espace fournisseur, tableau de bord administrateur, écrans intermédiaires d'accès, flux d'abonnement et d'achat.

**Documentation technique.** Le présent cahier des charges, le document d'architecture technique, la conception de la base de données, les scénarios d'utilisation, le plan de tests et le rapport de tests, et le design system.

**Mémoire académique.** Mémoire de licence rédigé par l'équipe, chaque membre contribuant à la description de son domaine de responsabilité.

---

## 14. Références bibliographiques

Anderson, C. (2009). *Free: The Future of a Radical Price*. Hyperion. ISBN 978-1401322908.

Apple Inc. (2025). *Human Interface Guidelines — iOS and iPadOS*. https://developer.apple.com/design/human-interface-guidelines

Chodorow, K. (2019). *MongoDB: The Definitive Guide* (3e éd.). O'Reilly Media. ISBN 978-1491954461.

DataReportal. (2025). *Digital 2025 : Madagascar*. Kepios Analysis. https://datareportal.com/reports/digital-2025-madagascar

Expo. (2025). *Expo Documentation — SDK 52*. https://docs.expo.dev

Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures* (Thèse de doctorat). University of California, Irvine. https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm

Google. (2025). *Material Design 3*. https://m3.material.io

Kumar, V. (2014). Making "Freemium" Work. *Harvard Business Review*, 92(5), 27–29.

Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall. ISBN 978-0134494166.

Mongoose. (2025). *Mongoose v8.x Documentation*. https://mongoosejs.com/docs

Newman, S. (2021). *Building Microservices* (2e éd.). O'Reilly Media. ISBN 978-1492034025.

OWASP Foundation. (2023). *OWASP Top Ten 2023*. https://owasp.org/www-project-top-ten/

Pressman, R. S., & Maxim, B. R. (2019). *Software Engineering: A Practitioner's Approach* (9e éd.). McGraw-Hill Education. ISBN 978-1259872976.

React. (2025). *React 18 — Documentation officielle*. https://react.dev

Stripe Inc. (2026). *Stripe API Reference — PaymentIntents*. https://stripe.com/docs/api/payment_intents

Stripe Inc. (2026). *Testing Stripe integrations*. https://stripe.com/docs/testing

Tailwind CSS. (2025). *Tailwind CSS v3 Documentation*. https://tailwindcss.com/docs

UNESCO. (2023). *Culture numérique et diversité culturelle dans les pays en développement*. UNESCO Publishing.

Vite. (2025). *Vite — Documentation officielle*. https://vitejs.dev/guide

W3C. (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*. https://www.w3.org/TR/WCAG21
