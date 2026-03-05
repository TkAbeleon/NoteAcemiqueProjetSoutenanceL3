# Scénarios Utilisateur — StreamMG

**Document :** Scénarios d'utilisation  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026

---

## 1. Introduction

Ce document décrit les scénarios d'utilisation principaux de StreamMG. Chaque scénario précise l'acteur concerné, la plateforme (mobile, web, ou les deux), les préconditions, le déroulement nominal, et les cas alternatifs.

**Rappel des niveaux d'accès :** gratuit = lisible par tous y compris les visiteurs ; premium = réservé aux abonnés Premium ; payant = achat unitaire requis, indépendant de l'abonnement ; tutoriel = mêmes règles d'accès avec suivi de progression supplémentaire.

---

## 2. Acteurs

Le **visiteur** accède sans compte et lit uniquement les contenus gratuits.

L'**utilisateur standard** est inscrit gratuitement. Il lit les contenus gratuits et peut acheter des contenus payants à l'unité.

L'**utilisateur premium** dispose d'un abonnement actif. Il accède aux contenus gratuits et premium, et peut acheter des contenus payants à l'unité.

Le **fournisseur** uploade des contenus, définit leur niveau d'accès et leur prix, et organise les tutoriels en séries de leçons.

L'**administrateur** valide les soumissions, gère le catalogue et consulte les statistiques.

---

## 3. Scénarios

### U-01 — Inscription

**Acteur :** Visiteur — **Plateforme :** Mobile et Web

L'utilisateur remplit le formulaire d'inscription (nom d'utilisateur, email, mot de passe ≥8 caractères avec majuscule et chiffre). La validation côté client signale les critères non satisfaits en temps réel. À la soumission, le backend valide les données, hache le mot de passe (bcrypt, coût 12), crée le compte avec rôle "user" et isPremium à false, retourne un JWT (15 min) et un refresh token (7 jours). L'utilisateur est connecté et redirigé.

**Cas alternatifs :** Email déjà utilisé → 409 "Adresse déjà utilisée". Mot de passe trop faible → validation côté client avant soumission.

---

### U-02 — Navigation dans le catalogue et découverte des niveaux d'accès

**Acteur :** Utilisateur standard — **Plateforme :** Mobile et Web

L'utilisateur parcourt le catalogue. Il voit trois types de contenus : sans badge (gratuits), badge or "★ Premium", badge teal "8 000 Ar". Clic sur gratuit → lecture immédiate. Clic sur premium → écran intermédiaire "Abonnez-vous à Premium" avec boutons "S'abonner" et "Fermer". Clic sur payant → écran "Acheter — 8 000 Ar" avec boutons "Acheter" et "Fermer".

**Cas alternatifs :** Visiteur non inscrit sur contenu premium → invitation à créer un compte. Utilisateur premium sur contenu payant → écran d'achat (l'abonnement ne couvre pas les contenus payants).

---

### U-03 — Souscription à l'abonnement Premium

**Acteur :** Utilisateur standard — **Plateforme :** Mobile et Web

L'utilisateur sélectionne un plan (mensuel 5 000 Ar fictif, ou annuel 50 000 Ar fictif). POST /api/payment/subscribe → backend crée un PaymentIntent Stripe → retourne client_secret. Formulaire de carte : Stripe Elements sur web, CardField natif sur mobile. Carte de test 4242 4242 4242 4242 → confirmation → webhook Stripe → backend met à jour isPremium: true, role: "premium", premiumExpiry: J+30. Confirmation à l'utilisateur.

**Cas alternatifs :** Carte 4000 0000 0000 9995 → refus Stripe → message d'erreur → aucune modification en base.

---

### U-04 — Achat unitaire d'un contenu payant

**Acteur :** Utilisateur standard ou premium — **Plateforme :** Mobile et Web

L'utilisateur clique "Acheter — 8 000 Ar" sur la page de détail d'un film payant. POST /api/payment/purchase avec { contentId }. Backend : vérifie l'absence de doublon dans la collection purchases → crée un PaymentIntent Stripe avec `metadata: { type: "purchase", userId, contentId }` → retourne client_secret. L'utilisateur saisit la carte de test et confirme. Webhook Stripe "payment_intent.succeeded" avec metadata.type === "purchase" → backend crée un document dans purchases → accès débloqué immédiatement. Le bouton "Acheter" devient "Lire". Accès permanent.

**Cas alternatifs :** Doublon → 409 "Vous avez déjà acheté ce contenu". Paiement échoué → aucun document créé dans purchases.

---

### U-05 — Accès refusé : écrans intermédiaires selon le profil

**Acteur :** Utilisateur standard et premium — **Plateforme :** Mobile et Web

**Cas A — Standard face à du premium :** checkAccess retourne 403 `reason: "subscription_required"` → écran "Abonnez-vous à Premium".

**Cas B — Standard face à du payant :** checkAccess retourne 403 `reason: "purchase_required"` avec le prix → écran d'achat avec le montant.

**Cas C — Premium face à du payant :** Même comportement que B. L'abonnement Premium ne couvre jamais les contenus payants. Ce point est fondamental à démontrer en soutenance.

---

### U-06 — Lecture d'un tutoriel avec suivi de progression

**Acteur :** Utilisateur ayant l'accès — **Plateforme :** Mobile et Web

**Précondition :** Le tutoriel "Cuisine malgache — 6 leçons" est accessible (gratuit).

L'utilisateur ouvre le tutoriel. Il voit la liste des 6 leçons et l'indicateur "0 % complété". Il clique leçon 1. La progression est envoyée toutes les 10 s. À 90 % de la durée → POST /api/tutorial/progress/:tutorialId `{ lessonIndex: 0, completed: true }` → backend crée/met à jour tutorialProgress : completedLessons: [0], percentComplete: 17. Bouton "Leçon suivante" s'affiche.

**Post-condition :** Profil affiche le tutoriel dans "Mes tutoriels en cours" avec 17 % de progression.

---

### U-07 — Reprise d'un tutoriel en cours

**Acteur :** Utilisateur — **Plateforme :** Mobile et Web

**Précondition :** L'utilisateur s'est arrêté à la leçon 3.

Accueil → section "Continuer" → tutoriel affiché avec "Leçon 3 — 33 % complété". Clic "Continuer" → GET /api/tutorial/progress détermine lastLessonIndex = 2 → leçon 3 chargée directement.

---

### U-08 — Upload d'un contenu payant par un fournisseur

**Acteur :** Fournisseur — **Plateforme :** Web

Le fournisseur sélectionne type "Vidéo — Film", remplit les métadonnées. Dans "Accès et monétisation", sélectionne "Payant" → le champ prix apparaît → saisit 7 500. Uploade le fichier et soumet. Backend crée le document : accessType: "paid", price: 750000 (centimes Stripe), isPublished: false. Message de confirmation "En attente de validation".

---

### U-09 — Upload d'un tutoriel en séries de leçons

**Acteur :** Fournisseur — **Plateforme :** Web

Le fournisseur sélectionne type "Tutoriel". Saisit le titre de la série, la description, la catégorie, le niveau d'accès. Clique "Ajouter des leçons" → interface de gestion : ajoute leçon 1 (lecon1.mp4), leçon 2 (lecon2.mp4), les réordonne par glisser-déposer. Soumet. Backend crée : isTutorial: true, lessons: [{order:1,...}, {order:2,...}].

---

### U-10 — Validation d'un contenu par l'administrateur

**Acteur :** Administrateur — **Plateforme :** Web

Section "En attente de validation" → film "Ny Fitiavana", payant, 8 000 Ar. L'admin visionne un extrait, juge le contenu conforme, ajuste le prix si nécessaire. Clique "Approuver et publier" → backend : isPublished: true → contenu visible dans le catalogue.

---

## 4. Références bibliographiques

Cockburn, A. (2000). *Writing Effective Use Cases*. Addison-Wesley Professional. ISBN 978-0201702255.

Stripe Inc. (2026). *Testing Stripe integrations*. https://stripe.com/docs/testing

Anderson, C. (2009). *Free: The Future of a Radical Price*. Hyperion. ISBN 978-1401322908.

Expo. (2025). *expo-file-system Documentation*. https://docs.expo.dev/versions/latest/sdk/filesystem
