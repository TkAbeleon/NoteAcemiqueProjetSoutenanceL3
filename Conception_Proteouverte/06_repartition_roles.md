# Répartition des Rôles et Planning — StreamMG

**Document :** Organisation de l'équipe, responsabilités et planning  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026

---

## 1. Principe d'organisation

L'équipe est composée de trois membres, chacun spécialisé dans un domaine technique distinct. Cette organisation reproduit le modèle des équipes de développement professionnelles : une équipe mobile, une équipe web, et une équipe backend/API. Les trois membres travaillent en parallèle à partir d'un contrat d'API commun produit par le Membre 3 en début de projet.

Le contrat d'API est le document de coordination central. Il liste l'ensemble des endpoints, les formats de requête et de réponse, les codes d'erreur, et les schémas de données. Les Membres 1 et 2 peuvent développer leurs interfaces en parallèle en mockant les réponses pendant les premières semaines, puis intégrer le vrai backend lorsque les modules fondamentaux sont disponibles.

---

## 2. Responsabilités détaillées

### Membre 1 — Développeur Frontend Mobile (38 %)

**Domaine :** Application React Native + Expo SDK 52

Le Membre 1 est responsable de l'intégralité de l'application mobile. Cela inclut l'architecture de navigation (expo-router, file-based routing), les écrans d'authentification, le catalogue avec les cartes de contenu et leurs badges de niveau d'accès (gratuit sans badge, premium badge or "★ Premium", payant badge teal avec prix en ariary), les lecteurs vidéo (expo-av en mode portrait et paysage automatique via expo-screen-orientation) et audio (expo-av), le mini-player audio persistant au-dessus de la tab bar, les playlists, l'historique de lecture, et le profil utilisateur.

Pour les fonctionnalités spécifiques au modèle économique, le Membre 1 implémente les trois écrans intermédiaires d'accès : écran d'invitation à l'abonnement (affiché quand `reason: "subscription_required"`), écran d'achat unitaire avec prix (affiché quand `reason: "purchase_required"` avec le prix retourné dans la réponse 403), et écran d'invitation à la connexion (affiché quand `reason: "login_required"`). Il intègre le flux d'achat unitaire via @stripe/stripe-react-native (composant CardField natif), en utilisant le même `StripeProvider` que l'abonnement. Il développe les interfaces de tutoriels : page de détail avec la liste des leçons ordonnées, lecteur de leçon individuelle avec barre de progression et indicateur de complétion, bouton "Continuer" redirigeant vers la dernière leçon non terminée, et section "Mes tutoriels en cours" dans le profil.

Le Membre 1 gère également le mode hors-ligne audio via expo-file-system (téléchargement dans documentDirectory, chemin local sauvegardé dans AsyncStorage) et la persistance de session via expo-secure-store pour le refresh token.

### Membre 2 — Développeur Frontend Web (32 %)

**Domaine :** Application React.js 18 + Vite 5

Le Membre 2 est responsable de l'intégralité de l'application web. Il développe les mêmes fonctionnalités que le Membre 1, adaptées au web : navigation SPA (react-router-dom v6), catalogue responsive, lecteurs react-player (vidéo et audio HTML5), mini-player persistant (rendu dans App.tsx hors du RouterProvider pour ne jamais être démonté lors des navigations), playlists, historique, profil.

Pour le modèle économique, le Membre 2 implémente les mêmes écrans intermédiaires que le Membre 1 (composants React overlay ou pages de redirection), le flux d'achat unitaire via Stripe Elements (@stripe/react-stripe-js, iframe sécurisée), et les pages de tutoriels avec liste de leçons et barre de progression globale.

Le Membre 2 est également responsable de l'interface d'upload pour les fournisseurs : formulaire avec le champ "Niveau d'accès" (menu déroulant : Gratuit, Premium, Payant), le champ de prix conditionnel (visible uniquement si "Payant" est sélectionné), et le gestionnaire de leçons pour les tutoriels (ajout, réordonnancement par glisser-déposer, suppression de leçons).

Il gère le mode hors-ligne via Service Worker (stratégie Cache First, expiration 48h, intégration Workbox) et la persistance de session via cookie httpOnly (géré automatiquement par le navigateur).

### Membre 3 — Développeur Backend + Coordination (30 %)

**Domaine :** API REST Node.js/Express + MongoDB + Sécurité + Infrastructure

Le Membre 3 est responsable de l'intégralité du backend et de la coordination technique générale. Il produit en semaine 1 le contrat d'API complet qui permet aux Membres 1 et 2 de travailler en parallèle.

Il développe toutes les routes de l'API (authentification, catalogue, historique, progression, paiement, fournisseur, administration), les huit collections MongoDB avec leurs schémas Mongoose, index et contraintes d'unicité, le middleware `checkAccess` (cœur du modèle économique, décrit en détail dans le document d'architecture), le middleware d'authentification JWT, le middleware de vérification des rôles (user, premium, provider, admin), Multer pour les uploads de fichiers, music-metadata pour l'extraction automatique des métadonnées ID3, le SDK Stripe pour les abonnements et les achats unitaires, le handler de webhook Stripe (distinguant les événements d'abonnement et d'achat via `metadata.type`), et l'ensemble de la sécurité applicative (bcrypt, helmet, CORS, rate-limit, express-validator).

Il déploie l'infrastructure : MongoDB Atlas, Railway (backend), Nginx (reverse proxy + SSL Let's Encrypt), et configure Vercel pour le frontend web (règle rewrite SPA). Il exporte la collection Postman complète.

---

## 3. Planning prévisionnel — 10 semaines

| Semaine | Membre 1 — Mobile | Membre 2 — Web | Membre 3 — Backend |
|---|---|---|---|
| **S1** | Init projet Expo, structure expo-router, maquettes Figma mobile | Init projet Vite + Tailwind, structure SPA, maquettes Figma web | **Contrat d'API complet**, schémas MongoDB, init Express, modèles Mongoose de base |
| **S2** | Composants de base, layouts, navigation tab bar, design system NativeWind | Composants de base, layouts, navigation react-router, design system Tailwind | Middleware auth (JWT + refresh token), routes /auth, configuration Multer |
| **S3** | Écrans auth (login, register, session persistante expo-secure-store), zustand authStore | Pages auth (login, register, session cookie httpOnly), zustand authStore | Routes /contents (CRUD, upload, pagination, filtres), index MongoDB |
| **S4** | Catalogue, ContentCard avec badges niveaux d'accès, recherche, filtres | Catalogue, ContentCard avec badges niveaux d'accès, recherche, filtres | Routes /history, /tutorial/progress, middleware checkAccess |
| **S5** | Lecteurs expo-av (vidéo + audio), paysage, mini-player persistant | Lecteurs react-player (vidéo + audio), mini-player App.tsx persistant | Routes /admin, /provider, statistiques, déploiement staging Railway |
| **S6** | Hors-ligne expo-file-system, téléchargement audio, AsyncStorage | Service Worker PWA (Workbox), Cache First audio 48h, installation PWA | Stripe subscribe + purchase (PaymentIntent, webhook, metadata.type) |
| **S7** | Stripe CardField, écrans intermédiaires (premium/payant/login), interfaces tutoriels | Stripe Elements, écrans intermédiaires (premium/payant/login), pages tutoriels | Extension routes fournisseur (accessType, price, leçons), tests Postman |
| **S8** | Interface fournisseur mobile, playlists, profil complet | Interface fournisseur web (champs prix conditionnels, gestionnaire leçons), admin web | Collection Postman exportée, corrections anomalies backend, sécurité complète |
| **S9** | Tests interface mobile (appareils iOS + Android), correction anomalies | Tests interface web (Chrome, Firefox, Safari, responsivité 360px), corrections | Documentation finale, tests sécurité (rate-limit, headers, CORS, webhook) |
| **S10** | Préparation démonstration mobile, contribution mémoire | Préparation démonstration web, contribution mémoire | Finalisation mémoire et slides, déploiement production final |

### Dépendances critiques

Le middleware `checkAccess` (S4, Membre 3) est le prérequis des écrans intermédiaires des Membres 1 et 2 (S7). Les Membres 1 et 2 peuvent développer les écrans intermédiaires avec des réponses mockées (403 avec `reason`) pendant les semaines S5–S6 en attendant l'intégration réelle en S7.

Le contrat d'API complet (S1, Membre 3) est le prérequis de tout le développement des Membres 1 et 2. Tout changement de signature d'endpoint après S2 doit être immédiatement communiqué aux trois membres.

---

## 4. Références bibliographiques

Brooks, F. P. (1975). *The Mythical Man-Month: Essays on Software Engineering*. Addison-Wesley. ISBN 978-0201835953.

Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide*. Scrum.org. https://scrumguides.org

Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures* (Thèse de doctorat). University of California, Irvine.
