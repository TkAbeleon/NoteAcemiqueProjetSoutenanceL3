# Analyse du Projet — StreamMG

**Titre :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Niveau :** Licence 3 Génie Logiciel  
**Type :** Projet de groupe, obligatoire  
**Équipe :** 3 membres  
**Date :** Février 2026

---

## 1. Contexte et problématique

### 1.1 Patrimoine culturel malgache et absence numérique

Madagascar possède un patrimoine audiovisuel et musical d'une richesse exceptionnelle : le hira gasy (théâtre musical traditionnel des hautes terres), le salegy (musique populaire du nord), le tsapiky (rythmes du sud-ouest), le beko, les documentaires sur la biodiversité unique de l'île, les productions cinématographiques locales et les émissions culturelles radiophoniques. Ce patrimoine reste pourtant absent, ou quasi absent, des grandes plateformes internationales de diffusion numérique.

Netflix, Spotify ou YouTube Premium proposent des catalogues massivement orientés vers les productions occidentales. Les rares contenus africains ou malgaches qui y figurent représentent une fraction marginale de l'offre, inaccessible de surcroît pour une majorité de la population en raison du coût des abonnements et des contraintes de connectivité.

### 1.2 Contexte numérique malgache

Selon DataReportal (2025), Madagascar compte environ 18,2 millions de connexions mobiles actives (56,2 % de la population), mais seulement 6,6 millions d'internautes (20,4 %). Le mobile est donc le premier et souvent le seul terminal numérique accessible. La bande passante est inégale : connexion 4G disponible en zones urbaines mais coûteuse, 3G ou 2G en zones rurales.

Ces données structurelles imposent des décisions d'architecture précises : le mode hors-ligne est indispensable, l'adaptation au débit disponible est nécessaire, et le dark mode par défaut est préférable pour les écrans OLED (économie de batterie). Ces contraintes ne sont pas des limitations : ce sont les paramètres réels d'un projet pensé pour son marché cible.

### 1.3 Problématique

Comment concevoir, dans les contraintes d'un projet académique de Licence, une plateforme de diffusion audiovisuelle et éducative qui intègre un modèle économique freemium multi-niveaux, adaptée aux contraintes locales malgaches, et démontrant la maîtrise d'une architecture logicielle full-stack avec deux clients frontend distincts consommant une API commune ?

---

## 2. Objectifs du projet

### 2.1 Objectif principal

Développer une plateforme cross-platform de diffusion audiovisuelle et éducative malgache, accessible via une application mobile (React Native/Expo) et une application web (React.js/Vite), avec un modèle économique freemium à quatre niveaux d'accès aux contenus, une gestion des utilisateurs et des fournisseurs de contenu, et des paiements simulés via Stripe en mode test.

### 2.2 Objectifs secondaires

La plateforme doit proposer un catalogue de contenus multimédia organisé (films, chants, documentaires, podcasts, tutoriels) avec les niveaux d'accès appropriés. Elle doit permettre aux fournisseurs de définir eux-mêmes le niveau d'accès et le prix de leurs contenus. Elle doit offrir une expérience éducative cohérente pour les tutoriels avec suivi de progression. Elle doit simuler des achats unitaires de contenus payants via Stripe en mode test. Elle doit maintenir une cohérence d'expérience entre les deux plateformes.

---

## 3. Modèle économique

StreamMG adopte un modèle freemium multi-niveaux comprenant quatre catégories de contenus.

Le **contenu gratuit** est accessible à tous sans inscription ni paiement. C'est la vitrine de la plateforme, destinée à attirer de nouveaux utilisateurs et à rendre la culture malgache accessible au plus grand nombre. Le fournisseur choisit de rendre un contenu gratuit pour accroître sa visibilité.

Le **contenu premium** est accessible uniquement aux abonnés Premium. L'abonnement donne accès à l'ensemble du catalogue premium — films, albums musicaux complets, documentaires, tutoriels premium — de manière illimitée pendant la durée de l'abonnement. Ce modèle est identique à celui de Netflix ou Spotify : un forfait mensuel ou annuel donne accès à un catalogue entier.

Le **contenu payant** est un achat unitaire, indépendant de tout abonnement. Que l'utilisateur soit standard ou Premium, il doit payer ce contenu séparément. L'accès est permanent une fois l'achat effectué. Ce niveau est conçu pour des contenus à forte valeur ajoutée : une master class d'un artiste reconnu, un film en avant-première, un événement exceptionnel.

Le **tutoriel** suit le même système d'accès (gratuit, premium ou payant), mais avec une logique de progression spécifique : les tutoriels sont organisés en séries de leçons ordonnées et la plateforme enregistre la progression de chaque utilisateur.

C'est le fournisseur de contenu qui, lors de l'upload, définit le niveau d'accès de son contenu et le prix unitaire si payant. Cette décision est soumise à la validation de l'administrateur avant publication.

---

## 4. Périmètre fonctionnel

### 4.1 Fonctionnalités incluses dans le MVP

Le catalogue propose les catégories : films malgaches, séries télévisées, musique traditionnelle (hira gasy, salegy, tsapiky, beko), musique contemporaine, documentaires, podcasts et émissions culturelles, et tutoriels (musique, cuisine, langue, artisanat, technologie). Chaque contenu porte son niveau d'accès et son prix si payant.

Le système d'accès multi-niveaux est vérifié côté backend par un middleware dédié (`checkAccess`) avant chaque accès à un fichier média. Les droits sont vérifiés selon le rôle du JWT (pour les contenus premium) ou selon l'existence d'un achat en base de données (pour les contenus payants).

Les tutoriels sont organisés en séries de leçons ordonnées. La plateforme enregistre la dernière leçon consultée et le pourcentage de complétion pour chaque utilisateur. Une section "Mes tutoriels en cours" est disponible dans le profil.

Le flux d'achat unitaire d'un contenu payant est simulé via Stripe en mode test. L'achat est enregistré dans la collection MongoDB `purchases`. L'accès est permanent et indépendant de tout abonnement futur ou de son absence.

L'espace fournisseur permet de définir le niveau d'accès et le prix de chaque contenu, et d'organiser les tutoriels en séries de leçons via une interface dédiée.

Le mode hors-ligne est disponible sur les deux plateformes : Service Worker PWA (stratégie Cache First, expiration 48h) sur le web, expo-file-system avec stockage local sur mobile.

### 4.2 Fonctionnalités exclues

Restent hors périmètre : les paiements en production (clés Stripe live), le streaming live, la recommandation par algorithme, la protection DRM avancée, la publication sur les stores Apple et Google, le système de commission pour les fournisseurs, et les certifications de complétion de tutoriels.

---

## 5. Architecture générale

L'architecture adopte le pattern multi-client avec backend partagé. Deux clients frontend distincts et indépendants consomment la même API REST Node.js/Express.

```
[App Mobile — React Native/Expo]     [App Web — React.js/Vite]
        Membre 1                              Membre 2
              \                                  /
               ———————[ HTTPS / REST JSON + JWT ]———————
                                   |
                     [API REST — Node.js/Express]
                           Membre 3
                          /         \
                    [MongoDB]   [/uploads — fichiers médias]
                                        |
                              [Stripe API — mode test]
```

Cette architecture est représentative des pratiques professionnelles des équipes de développement en entreprise : équipes mobile et web spécialisées, travaillant en parallèle sur le même produit à partir d'un contrat d'API commun.

---

## 6. Répartition des rôles

**Membre 1 — Développeur Frontend Mobile (38 %).** Intégralité de l'application React Native/Expo : navigation, lecteurs vidéo et audio natifs, mini-player persistant, mode hors-ligne (expo-file-system), affichage des badges de niveau d'accès, écrans intermédiaires d'accès, flux d'achat Stripe sur mobile, interfaces de tutoriels avec progression.

**Membre 2 — Développeur Frontend Web (32 %).** Intégralité de l'application React.js/Vite : navigation SPA, lecteurs react-player, mini-player persistant, Service Worker PWA, affichage des badges, écrans intermédiaires, Stripe Elements, pages de tutoriels avec barre de progression, responsivité complète.

**Membre 3 — Développeur Backend + Coordination (30 %).** Intégralité de l'API REST : authentification JWT, catalogue, historique, achats, tutoriels ; middleware checkAccess, sécurité (bcrypt, helmet, CORS, rate-limit, validation) ; MongoDB/Mongoose (8 collections) ; Stripe SDK (abonnement et achats unitaires) ; webhook Stripe ; Nginx + SSL ; contrat d'API ; coordination générale.

---

## 7. Planning prévisionnel — 10 semaines

| Semaine | Membre 1 — Mobile | Membre 2 — Web | Membre 3 — Backend |
|---|---|---|---|
| S1 | Init projet Expo, maquettes Figma mobile | Init projet Vite, maquettes Figma web | Contrat d'API complet, schémas MongoDB, init projet |
| S2 | Composants de base, navigation expo-router | Composants de base, react-router-dom | Modèles Mongoose, middleware auth, routes auth |
| S3 | Écrans auth, zustand authStore, session | Pages auth, zustand authStore, session | Routes contents, upload Multer, music-metadata |
| S4 | Catalogue, cartes avec badges, recherche | Catalogue, cartes avec badges, recherche | Routes history, tutorialProgress, checkAccess |
| S5 | Lecteurs expo-av, paysage vidéo, mini-player | Lecteurs react-player, mini-player App.tsx | Routes admin, provider, statistiques |
| S6 | Hors-ligne expo-file-system, téléchargement | Service Worker PWA, Cache First audio | Stripe subscribe + purchase, webhook |
| S7 | Stripe CardField, écrans accès premium/payant | Stripe Elements, écrans accès premium/payant | Déploiement Railway + Nginx + SSL staging |
| S8 | Interface fournisseur mobile, tutoriels | Interface fournisseur web, tutoriels | Tests API Postman complets, corrections |
| S9 | Tests interface mobile, corrections | Tests interface web, corrections | Collection Postman exportée, doc finale |
| S10 | Préparation démonstration mobile | Préparation démonstration web | Finalisation mémoire, slides soutenance |

---

## 8. Références bibliographiques

DataReportal. (2025). *Digital 2025 : Madagascar*. Kepios Analysis. https://datareportal.com/reports/digital-2025-madagascar

Anderson, C. (2009). *Free: The Future of a Radical Price*. Hyperion. ISBN 978-1401322908.

Kumar, V. (2014). Making "Freemium" Work. *Harvard Business Review*, 92(5), 27–29.

Chodorow, K. (2019). *MongoDB: The Definitive Guide* (3e éd.). O'Reilly Media. ISBN 978-1491954461.

Expo. (2025). *Expo Documentation — SDK 52*. https://docs.expo.dev

Vite. (2025). *Vite Documentation*. https://vitejs.dev/guide

OWASP Foundation. (2023). *OWASP Top Ten 2023*. https://owasp.org/www-project-top-ten/

UNESCO. (2023). *Culture numérique et diversité culturelle dans les pays en développement*. UNESCO Publishing.

Newman, S. (2021). *Building Microservices* (2e éd.). O'Reilly Media. ISBN 978-1492034025.

Pressman, R. S., & Maxim, B. R. (2019). *Software Engineering: A Practitioner's Approach* (9e éd.). McGraw-Hill Education. ISBN 978-1259872976.
