# Authentification, rôles et accès

## Inscription
Le flux frontend d'inscription comprend la création du compte, la demande d'OTP email, la vérification puis l'ouverture de session.

## JWT
Le backend utilise un jeton pour les appels authentifiés. Le frontend le conserve côté client.

## Rôles
Les rôles observés sont :
- `standard`
- `premium`
- `admin`

## Premium
Le rôle Premium ouvre notamment des fonctions supplémentaires comme les zones surveillées et les canaux SMS/WhatsApp.

## Administrateur
L'Admin dispose notamment de fonctions de gestion des utilisateurs, demandes d'accès et opérations internes du pipeline.

## Demandes d'accès
Le backend possède un workflow de demande d'accès pouvant évoluer vers approbation ou rejet. L'approbation peut accorder le niveau Premium selon le flux actuel.

## OTP d'abonnement
La vérification des destinations d'alerte est distincte de la session JWT. L'OTP d'abonnement expire après 5 minutes et est limité à trois tentatives.

## Protection administrative
Le backend contient une logique de protection du dernier administrateur actif.

## Principe
> L'authentification établit l'identité ; le rôle détermine les capacités ; les routes backend appliquent le contrôle final.