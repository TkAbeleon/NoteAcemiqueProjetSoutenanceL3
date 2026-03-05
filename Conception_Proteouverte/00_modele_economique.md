# Modèle Économique — StreamMG

**Document :** Définition du modèle économique et règles d'accès aux contenus  
**Projet :** StreamMG — Plateforme de streaming audiovisuel et éducatif malagasy  
**Date :** Février 2026

---

## 1. Vue d'ensemble

StreamMG adopte un modèle économique **freemium multi-niveaux**. Ce modèle, utilisé par des plateformes comme Spotify ou YouTube, combine une offre gratuite accessible au plus grand nombre avec des offres monétisées qui rémunèrent les fournisseurs de contenu et assurent la viabilité économique de la plateforme. Il est particulièrement adapté au contexte malgache, où le pouvoir d'achat est variable et où l'accessibilité culturelle est un objectif explicite du projet.

---

## 2. Les quatre niveaux d'accès

### Niveau 1 — Contenu gratuit

Accessible à toute personne visitant la plateforme, inscrite ou non, abonnée ou non. C'est le fournisseur qui décide de rendre un contenu gratuit lors de l'upload — souvent pour accroître sa visibilité ou attirer une audience. Les contenus gratuits constituent la vitrine de la plateforme et sont listés sans restriction dans le catalogue. Leur lecture ne requiert aucune authentification, bien que les utilisateurs connectés bénéficient de l'enregistrement de leur historique.

### Niveau 2 — Contenu premium

Accessible uniquement aux abonnés Premium. L'abonnement donne accès à l'ensemble du catalogue premium — films, albums musicaux complets, documentaires, tutoriels premium — de manière illimitée pendant sa durée. Ce modèle est analogue à Netflix : un forfait mensuel ou annuel donne accès à un catalogue entier.

### Niveau 3 — Contenu payant (achat unitaire)

Accessible après un achat unitaire permanent, indépendant de tout abonnement. Un utilisateur standard **et** un utilisateur Premium doivent payer ce contenu séparément — l'abonnement ne couvre jamais les contenus payants. Une fois acheté, l'accès est permanent, quelle que soit l'évolution du statut d'abonnement de l'utilisateur. Ce niveau est conçu pour des contenus à forte valeur ajoutée : avant-premières, master classes, événements exclusifs. Le fournisseur fixe lui-même le prix unitaire.

### Niveau 4 — Tutoriel

Les tutoriels suivent le même système d'accès (gratuit, premium ou payant) avec une logique fonctionnelle supplémentaire : ils sont organisés en séries de leçons ordonnées. La plateforme mémorise la progression de chaque utilisateur (dernière leçon consultée, pourcentage complété). Cette progression est disponible pour tous les niveaux d'accès.

---

## 3. Tableau synthétique des droits d'accès

| Type de contenu | Visiteur | Standard | Premium | Remarque |
|---|---|---|---|---|
| Gratuit | OUI | OUI | OUI | Aucune restriction |
| Premium | NON | NON | OUI | Abonnement requis |
| Payant (unitaire) | NON | ACHAT | ACHAT | Indépendant de l'abonnement |
| Tutoriel gratuit | OUI | OUI | OUI | + progression trackée |
| Tutoriel premium | NON | NON | OUI | + progression trackée |
| Tutoriel payant | NON | ACHAT | ACHAT | + progression trackée |

**Point critique :** la cellule "ACHAT" pour la colonne Premium sur les contenus payants est fondamentale. Elle signifie qu'un utilisateur Premium qui tente d'accéder à un contenu payant reçoit exactement le même écran d'achat qu'un utilisateur standard. Le middleware `checkAccess` applique cette règle côté serveur, indépendamment du rôle contenu dans le JWT.

---

## 4. Rôle du fournisseur dans le modèle

Le fournisseur est l'acteur central du modèle économique. Pour chaque contenu uploadé, il décide du niveau d'accès (gratuit, premium, payant) et fixe le prix si payant. Cette décision est soumise à la validation d'un administrateur avant publication. Le fournisseur peut modifier le niveau d'accès après publication, sous réserve d'une nouvelle validation.

---

## 5. Simulation des paiements

Tous les paiements — abonnement Premium et achats unitaires — sont simulés via Stripe en mode test. Aucune transaction financière réelle n'est effectuée. Les prix sont fictifs, exprimés en ariary malgache symbolique. Les cartes de test Stripe utilisées en démonstration : **4242 4242 4242 4242** (paiement accepté), **4000 0000 0000 9995** (paiement refusé).

Ce choix est académiquement défendable : il illustre une intégration technique réelle et complète d'un système de paiement (création de PaymentIntent, confirmation côté client, réception du webhook) sans nécessiter d'agrément de prestataire de services de paiement.

---

## 6. Références bibliographiques

Anderson, C. (2009). *Free: The Future of a Radical Price*. Hyperion. ISBN 978-1401322908.

Kumar, V. (2014). Making "Freemium" Work. *Harvard Business Review*, 92(5), 27–29.

Stripe Inc. (2026). *Stripe API Reference — PaymentIntents*. https://stripe.com/docs/api/payment_intents

Stripe Inc. (2026). *Stripe Testing Documentation*. https://stripe.com/docs/testing
