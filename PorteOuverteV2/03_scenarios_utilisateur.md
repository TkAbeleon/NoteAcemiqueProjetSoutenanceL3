# Scenarios Utilisateur — StreamMG

**Document :** Scenarios d'utilisation et cas d'usage  
**Projet :** StreamMG — Plateforme de streaming audiovisuel malagasy  
**Version :** 1.0  
**Date :** Fevrier 2026

---

## 1. Introduction

Ce document decrit les scenarios d'utilisation principaux de la plateforme StreamMG. Chaque scenario est redige du point de vue de l'utilisateur final, avec une description du contexte, des pre-conditions, du deroulement pas a pas, des post-conditions, et des cas alternatifs ou d'erreur. Ces scenarios servent de base pour la conception des maquettes, la redaction des tests fonctionnels, et la preparation de la soutenance.

---

## 2. Acteurs

**Visiteur :** Toute personne accedant a la plateforme sans etre connectee. Il peut consulter le catalogue en mode apercu mais ne peut pas lire les contenus.

**Utilisateur standard :** Personne inscrite et connectee avec un compte gratuit. Il peut lire les contenus dans les limites du plan gratuit (5 contenus par jour).

**Utilisateur premium :** Personne inscrite, connectee, et ayant souscrit au plan Premium simule. Il beneficie d'un acces illimite aux contenus et d'une qualite de lecture superieure.

**Administrateur :** Membre de l'equipe disposant de droits eleves pour gerer le catalogue complet, consulter les statistiques globales, et approuver les contenus soumis par les fournisseurs.

**Fournisseur de contenu :** Producteur ou detenteur de droits culturels malgaches disposant d'un compte "provider". Il peut uploader et gerer ses propres contenus uniquement, et attend l'approbation d'un administrateur avant leur publication.

---

## 3. Scenarios d'utilisation

### Scenario U-01 : Inscription d'un nouvel utilisateur

**Acteur principal :** Visiteur  
**Objectif :** Creer un compte sur la plateforme pour acceder aux contenus  
**Pre-condition :** L'utilisateur n'a pas encore de compte et accede a la plateforme depuis un navigateur web ou l'application mobile

**Deroulement nominal :**

L'utilisateur arrive sur la page d'accueil de StreamMG. Il clique sur le bouton "S'inscrire" visible dans la barre de navigation. Il arrive sur la page d'inscription et remplit le formulaire avec son nom d'utilisateur, son adresse email et un mot de passe respectant les criteres de securite (8 caracteres minimum, une majuscule, un chiffre). Il clique sur "Creer mon compte". Le systeme valide les donnees, hache le mot de passe avec bcrypt, cree l'entree dans la collection users de MongoDB, et retourne une reponse de succes. L'utilisateur est automatiquement connecte et redirige vers la page d'accueil en tant qu'utilisateur authentifie.

**Post-condition :** Un compte utilisateur actif existe en base de donnees. L'utilisateur est connecte et dispose d'un JWT valide stocke en memoire et d'un refresh token en cookie httpOnly.

**Cas alternatifs :**

Si l'adresse email est deja associee a un compte existant, le systeme affiche un message d'erreur explicite : "Cette adresse email est deja utilisee". Le formulaire reste pre-rempli avec les donnees valides pour eviter a l'utilisateur de tout ressaisir. Si le mot de passe ne respecte pas les criteres, un message d'aide est affiche en temps reel (validation cote client) avant meme la soumission du formulaire.

---

### Scenario U-02 : Connexion d'un utilisateur existant

**Acteur principal :** Utilisateur standard ou premium  
**Objectif :** Acceder a son compte pour reprendre la navigation  
**Pre-condition :** L'utilisateur dispose d'un compte valide et non desactive

**Deroulement nominal :**

L'utilisateur arrive sur la page de connexion. Il saisit son adresse email et son mot de passe. Il clique sur "Se connecter". Le backend recoit la requete, retrouve l'utilisateur par son email en base de donnees, compare le mot de passe fourni au hash stocke via bcrypt.compare(), genere un JWT (duree de validite : 15 minutes) contenant l'identifiant et le role de l'utilisateur, genere un refresh token (duree de validite : 7 jours) stocke en base de donnees sous forme hachee, et retourne le JWT dans le corps de la reponse et le refresh token dans un cookie httpOnly securise. L'utilisateur est redirige vers la page d'accueil en mode authentifie.

**Post-condition :** L'utilisateur est authentifie. Son JWT lui permet d'acceder aux routes protegees de l'API pendant 15 minutes. Son refresh token lui permettra de renouveler automatiquement son JWT sans se reconneccer pendant 7 jours.

**Cas alternatifs :**

Si le mot de passe est incorrect, le systeme retourne une reponse generique "Identifiants incorrects" sans preciser si c'est l'email ou le mot de passe qui est errone (securite contre l'enumeration de comptes). Apres 5 tentatives de connexion echouees depuis la meme IP dans une fenetre de 15 minutes, le rate limiter bloque temporairement les nouvelles tentatives.

---

### Scenario U-03 : Recherche et selection d'un contenu

**Acteur principal :** Utilisateur standard  
**Objectif :** Trouver un film ou un titre musical specifique et commencer sa lecture  
**Pre-condition :** L'utilisateur est connecte

**Deroulement nominal :**

L'utilisateur arrive sur la page d'accueil et remarque la barre de recherche. Il saisit "salegy" dans le champ de recherche. Pendant la saisie, apres 300 millisecondes de pause (debounce pour eviter les requetes trop frequentes), le frontend envoie une requete GET /api/contents?search=salegy&type=audio a l'API backend. Le backend effectue une requete MongoDB avec un filtre de recherche textuelle sur les champs title et artist, retourne les resultats pagines (20 premiers resultats). Le frontend affiche les resultats sous forme de grille de cartes avec vignette, titre et artiste. L'utilisateur clique sur un titre qui l'interesse. Il arrive sur la page de detail du contenu, qui affiche la description, la duree, l'artiste et le genre. Il clique sur "Ecouter". Le lecteur audio se lance et le mini-player apparait en bas de l'ecran. L'utilisateur peut continuer a naviguer dans le catalogue pendant que la lecture se poursuit.

**Post-condition :** La lecture est en cours. L'historique de l'utilisateur est mis a jour en base de donnees avec la position de lecture toutes les 10 secondes (enregistrement periodique cote client avec une requete POST /api/history/:contentId).

**Cas alternatifs :**

Si la recherche ne retourne aucun resultat, l'interface affiche un message "Aucun contenu ne correspond a votre recherche" avec des suggestions de categories a explorer. Si la connexion reseau est perdue pendant la lecture audio, le mini-player passe en mode tampon puis affiche un message d'erreur avec un bouton "Reessayer".

---

### Scenario U-04 : Visionnage d'un film avec reprise automatique

**Acteur principal :** Utilisateur premium  
**Objectif :** Reprendre la lecture d'un film commence lors d'une session precedente  
**Pre-condition :** L'utilisateur est connecte en tant qu'utilisateur premium et a deja commence a regarder ce film

**Deroulement nominal :**

L'utilisateur ouvre l'application et arrive sur la page d'accueil. La section "Continuer a regarder" est visible en haut de la page et affiche le film en cours avec une barre de progression indiquant le pourcentage deja visionne. L'utilisateur clique sur ce film. Le frontend charge la page de detail et effectue une requete GET /api/history pour retrouver la position de lecture enregistree. Le lecteur video se charge et reprend automatiquement a la position enregistree (par exemple : 47 minutes et 23 secondes). L'utilisateur continue de regarder le film. Sa position est mise a jour toutes les 10 secondes en base de donnees via des requetes POST /api/history/:contentId envoyees en arriere-plan.

**Post-condition :** La position de lecture est mise a jour en base de donnees. Si l'utilisateur arrive a la fin du film, son entree dans l'historique est marquee comme "complete" et le contenu disparait de la section "Continuer a regarder".

**Cas alternatifs :**

Si l'utilisateur n'est pas premium et que le contenu est exclusif Premium, le lecteur video affiche un ecran de verrou avec un message "Ce contenu est reserve aux membres Premium" et un bouton de redirection vers la page d'abonnement simule.

---

### Scenario U-05 : Mise en cache hors-ligne d'un titre audio (Web)

**Acteur principal :** Utilisateur authentifie (standard ou premium)  
**Objectif :** Mettre en cache un titre audio pour l'ecouter sans connexion internet  
**Pre-condition :** L'utilisateur est connecte depuis un navigateur web compatible PWA (Chrome, Edge, Firefox). Le Service Worker est installe et actif.

**Deroulement nominal :**

L'utilisateur navigue dans le catalogue audio et trouve un titre qu'il souhaite ecouter hors-ligne. Il appuie sur l'icone de telechargement hors-ligne associee a la carte du contenu. Le frontend envoie une instruction au Service Worker pour mettre en cache le fichier audio (URL du fichier). Le Service Worker ouvre le cache de l'API Cache sous le nom "streamMG-offline-audio-v1", effectue une requete fetch vers l'URL du fichier audio, et stocke la reponse dans le cache avec un horodatage d'expiration de 48 heures. L'icone de telechargement se transforme en icone "disponible hors-ligne" (par exemple, une coche). L'utilisateur recoit une notification toast confirmant : "Titre disponible hors-ligne pendant 48 heures".

**Post-condition :** Le fichier audio est present dans le cache du navigateur. Lorsque l'utilisateur est hors connexion et tente de lire ce titre, le Service Worker intercepte la requete et sert le fichier depuis le cache sans contacter le serveur.

**Cas alternatifs :**

Si le fichier audio est superieur a la limite de stockage du cache (generalement 50 Mo par defaut selon le navigateur), le Service Worker retourne une erreur et l'interface affiche "Impossible de mettre en cache ce contenu (taille insuffisante)". Si 48 heures se sont ecoulees depuis la mise en cache, le Service Worker supprime automatiquement l'entree perimee et l'icone repasse a l'etat "non mis en cache".

---

### Scenario U-06 : Souscription au plan Premium simule

**Acteur principal :** Utilisateur standard (compte gratuit)  
**Objectif :** Souscrire au plan Premium pour acceder a l'ensemble du catalogue sans limitation  
**Pre-condition :** L'utilisateur est connecte. Il dispose des numeros de carte de test Stripe pour la demonstration.

**Deroulement nominal :**

L'utilisateur clique sur "Passer a Premium" dans son menu de profil ou sur le bandeau d'invitation visible lors d'une tentative d'acces a un contenu Premium. Il arrive sur la page de selection du plan. Il choisit entre l'abonnement mensuel (fictif : 5 000 Ar/mois) et l'abonnement annuel (fictif : 50 000 Ar/an). Il clique sur "Souscrire". Le frontend envoie une requete POST /api/payment/create-intent au backend StreamMG avec le plan selectionne. Le backend cree un PaymentIntent chez Stripe en mode test via l'API Stripe (stripe.paymentIntents.create({ amount: 500000, currency: 'mga', ... })) et retourne le client_secret dans la reponse. Le frontend recoit le client_secret et initialise le formulaire Stripe Elements avec. L'utilisateur saisit le numero de carte de test (4242 4242 4242 4242), la date d'expiration (toute date future) et le CVV (tout nombre a 3 chiffres). Il clique sur "Confirmer le paiement". Stripe.js appelle stripe.confirmCardPayment(clientSecret) cote client. Stripe valide le paiement en mode test et retourne un statut "succeeded". Le backend recoit la confirmation via le webhook Stripe (simule localement avec stripe listen ou via le tableau de bord Stripe test). Il met a jour le champ isPremium a true et le champ premiumExpiry a la date d'expiration calculee dans la collection users. L'utilisateur voit un ecran de confirmation "Bienvenue dans StreamMG Premium !" et est redirige vers la page d'accueil avec son statut Premium actif.

**Post-condition :** L'utilisateur a le statut isPremium = true en base de donnees. Il peut acceder a l'ensemble du catalogue sans limitation. Son statut Premium est visible dans son profil.

**Cas alternatifs :**

Si l'utilisateur saisit le numero de carte 4000 0000 0000 9995 (carte de test Stripe pour simuler un refus), Stripe retourne une erreur "Your card was declined". Le frontend affiche ce message d'erreur sous le formulaire. L'utilisateur peut reessayer avec une autre carte. Si l'utilisateur ferme la page pendant la saisie du formulaire, aucune modification n'est apportee a son statut en base de donnees. Le PaymentIntent Stripe en mode test est automatiquement annule par Stripe apres une periode d'inactivite.

---

### Scenario U-07 : Upload d'un contenu par l'administrateur

**Acteur principal :** Administrateur  
**Objectif :** Ajouter un nouveau titre audio dans le catalogue de la plateforme  
**Pre-condition :** L'administrateur est connecte avec un compte de role admin. Il dispose du fichier audio a uploader (format MP3, inferieur a 50 Mo) et de ses informations.

**Deroulement nominal :**

L'administrateur accede au tableau de bord via la route /admin. Il clique sur "Ajouter un contenu". Il choisit le type "Audio". Il remplit le formulaire : titre, description, categorie (salegy), langue (malgache). Il selectionne le fichier MP3 depuis son systeme de fichiers. Il selectionne optionnellement une vignette personnalisee. Il clique sur "Publier". Le frontend envoie une requete POST /api/admin/contents avec les donnees du formulaire et le fichier audio au format multipart/form-data. Le middleware Multer cote backend recoit le fichier, verifie son type MIME (audio/mpeg) et sa taille. Le backend passe le fichier a la librairie music-metadata pour extraire automatiquement les metadonnees ID3 : titre, artiste, album, duree, et pochette d'album encodee en base64 si presente dans les metadonnees du fichier. Le fichier est enregistre dans le repertoire /uploads/audio/ du serveur avec un nom unique genere (UUID). Un document est cree dans la collection contents de MongoDB avec toutes les metadonnees. Le backend retourne une reponse de succes avec l'ID du nouveau contenu. Le tableau de bord affiche le nouveau titre dans la liste des contenus.

**Post-condition :** Le titre audio est disponible dans le catalogue. Il apparait dans les resultats de recherche et dans la categorie correspondante. Les metadonnees ID3 ont ete extraites et sont affichees dans la fiche du contenu.

**Cas alternatifs :**

Si le fichier depasse la taille maximale autorisee (50 Mo pour les audios), Multer rejette l'upload et le backend retourne une erreur 413 avec le message "Fichier trop volumineux. Taille maximale : 50 Mo". Si le type MIME du fichier n'est pas audio/mpeg ou audio/aac, le backend retourne une erreur 400 "Format de fichier non supporte".

---

### Scenario U-08 : Consultation des statistiques par l'administrateur

**Acteur principal :** Administrateur  
**Objectif :** Consulter les performances du catalogue pour identifier les contenus les plus populaires  
**Pre-condition :** L'administrateur est connecte. Des utilisateurs ont consulte des contenus au cours des 7 derniers jours.

**Deroulement nominal :**

L'administrateur accede au tableau de bord /admin et clique sur l'onglet "Statistiques". Le frontend envoie une requete GET /api/admin/stats au backend. Le backend effectue des agregations MongoDB sur la collection watchHistory pour calculer : le top 10 des contenus les plus vus et ecoutes sur les 7 derniers jours, le top 10 sur les 30 derniers jours, le nombre total d'utilisateurs inscrits, le nombre d'utilisateurs ayant consulte au moins un contenu dans les 7 derniers jours (utilisateurs actifs). Le backend retourne ces donnees en JSON. Le frontend les affiche sous forme de tableaux et de graphiques en barres simples.

**Post-condition :** L'administrateur dispose d'une vue synthetique de l'utilisation de la plateforme, lui permettant de prioriser les ajouts de contenus dans les categories les plus consultees.

---


---

### Scenario U-09 : Upload d'un contenu par un fournisseur de contenu

**Acteur principal :** Fournisseur de contenu (role "provider")  
**Objectif :** Deposer un nouveau titre audio sur la plateforme pour le soumettre a la validation de l'administrateur  
**Pre-condition :** Le fournisseur dispose d'un compte actif avec le role "provider". Il est connecte. Il dispose d'un fichier MP3 de son contenu culturel (inferieur a 50 Mo).

**Deroulement nominal :**

Le fournisseur accede a son tableau de bord via la route /provider. Il clique sur "Deposer un contenu". Il choisit le type "Audio". Il remplit le formulaire avec le titre, la description, la categorie (par exemple "hira gasy"), la langue, et l'artiste. Il selectionne le fichier MP3. Il clique sur "Soumettre pour validation". Le frontend envoie une requete POST /api/provider/contents au backend. Le middleware `provider.middleware.js` verifie que le role de l'utilisateur est "provider" ou "admin". Le backend traite l'upload via Multer, extrait les metadonnees ID3 via music-metadata, et cree un document dans la collection contents avec le champ `isPublished: false` (en attente de validation) et `uploadedBy` egal a l'identifiant du fournisseur. Le fournisseur recoit une confirmation : "Votre contenu a ete soumis. Il sera visible apres validation par notre equipe."

**Post-condition :** Le contenu existe en base de donnees avec `isPublished: false`. Il n'est pas visible dans le catalogue public. Un administrateur peut le voir dans le tableau de bord admin et le publier ou le rejeter.

**Cas alternatifs :**

Si le fournisseur tente d'acceder a la route /api/admin/contents (route reservee aux administrateurs) avec son token "provider", le middleware `admin.middleware.js` retourne une reponse 403 Forbidden. Si le fournisseur tente de modifier un contenu dont `uploadedBy` ne correspond pas a son identifiant, le controller detecte cette tentative et retourne egalement une reponse 403 Forbidden.

---

### Scenario U-10 : Approbation d'un contenu fournisseur par l'administrateur

**Acteur principal :** Administrateur  
**Objectif :** Examiner un contenu soumis par un fournisseur et le publier dans le catalogue  
**Pre-condition :** Un fournisseur a soumis un contenu (scenario U-09). L'administrateur est connecte.

**Deroulement nominal :**

L'administrateur accede a son tableau de bord /admin et consulte la section "Contenus en attente de validation". Il voit le contenu soumis par le fournisseur avec ses metadonnees. Il ecoute un extrait ou consulte les informations. S'il juge le contenu conforme, il clique sur "Approuver et publier". Le frontend envoie une requete PUT /api/admin/contents/:id avec `{ "isPublished": true }`. Le backend met a jour le champ `isPublished` du document. Le contenu devient visible dans le catalogue public. Si l'administrateur juge le contenu non conforme, il clique sur "Rejeter" et peut laisser un commentaire optionnel. Le contenu reste `isPublished: false` et le fournisseur peut le corriger.

**Post-condition :** Le contenu est publie dans le catalogue avec `isPublished: true`. Il apparait dans les resultats de recherche et dans la categorie correspondante.

## 4. References bibliographiques

Cockburn, A. (2000). *Writing Effective Use Cases*. Addison-Wesley Professional. ISBN 978-0201702255.

Jacobson, I., Christerson, M., Jonsson, P., & Overgaard, G. (1992). *Object-Oriented Software Engineering: A Use Case Driven Approach*. Addison-Wesley. ISBN 978-0201544350.

Leffingwell, D., & Widrig, D. (2003). *Managing Software Requirements: A Use Case Approach* (2e ed.). Addison-Wesley Professional. ISBN 978-0321122933.

Stripe Inc. (2026). *Testing Stripe integrations — Test card numbers*. https://stripe.com/docs/testing#cards

Mozilla Developer Network. (2025). *Cache API*. https://developer.mozilla.org/en-US/docs/Web/API/Cache
