# Descriptions textuelles des diagrammes d'activité — JeryMotro

Les descriptions suivantes correspondent aux cas d'utilisation du diagramme de cas d'utilisation JeryMotro. Chaque description suit la structure du cours : précondition, postcondition, scénario nominal et, lorsque cela est nécessaire, scénario alternatif ou exceptionnel.

---

# DA1 — Consulter la carte de feux

## Généralité
- **Activité:** « Consulter la carte de feux »
- **Acteur principal:** Visiteur
- **Précondition:** La plateforme JeryMotro est accessible et les données de détection disponibles peuvent être consultées.
- **Début:** Le visiteur ouvre la carte de feux.
- **Postcondition:** Les détections correspondant aux critères sélectionnés sont affichées sur la carte.

## Scénario nominal
1. Le visiteur ouvre la carte de feux.
2. Le système affiche la carte et les outils de consultation.
3. Le visiteur sélectionne les critères de recherche ou de filtrage souhaités.
4. Le système recherche les détections correspondant aux critères sélectionnés.
5. Le système reçoit les données disponibles.
6. Le système affiche les détections sur la carte.
7. Le visiteur consulte les résultats.
8. Fin de l'activité.

## Scénario alternatif
### 4 - Aucun résultat
4.1. Le système ne trouve aucune détection correspondant aux critères sélectionnés.

4.2. Le système indique qu'aucune détection n'est disponible.

4.3. Le visiteur peut modifier les critères et relancer la consultation.

4.4. Reprise au point **3** du scénario nominal.

---

# DA2 — Voir les feux actifs

## Généralité
- **Activité:** « Voir les feux actifs »
- **Acteur principal:** Visiteur
- **Précondition:** Les données de feux sont disponibles dans JeryMotro.
- **Début:** Le visiteur demande l'affichage des feux actifs.
- **Postcondition:** Les feux actifs disponibles sont affichés.

## Scénario nominal
1. Le visiteur demande la consultation des feux actifs.
2. Le système récupère les données de feux disponibles.
3. Le système identifie les feux dont le statut est actif.
4. Le système prépare les informations associées aux feux retenus.
5. Le système affiche les feux actifs.
6. Fin de l'activité.

## Scénario alternatif
### 3 - Aucun feu actif
3.1. Le système ne trouve aucun feu actif.

3.2. Le système indique qu'aucun feu actif n'est disponible.

3.3. Fin de l'activité.

---

# DA3 — Créer un compte

## Généralité
- **Activité:** « Créer un compte »
- **Acteur principal:** Visiteur
- **Acteur secondaire:** Service d'envoi du code OTP
- **Précondition:** La page de création de compte est accessible.
- **Début:** Le visiteur ouvre le formulaire d'inscription.
- **Postcondition:** Le compte est créé et l'utilisateur est connecté lorsque la vérification OTP est réussie.

## Scénario nominal
1. Le visiteur ouvre la page de création de compte.
2. Le système affiche le formulaire d'inscription.
3. Le visiteur saisit ses informations, notamment son nom, son adresse e-mail, son organisation et son mot de passe.
4. Le visiteur valide le formulaire.
5. Le système vérifie que l'adresse e-mail n'est pas déjà utilisée.
6. L'adresse e-mail est disponible.
7. Le système génère un code OTP à six chiffres.
8. Le système envoie le code OTP à l'adresse e-mail fournie.
9. Le visiteur saisit le code OTP reçu.
10. Le système vérifie le code OTP.
11. Le code OTP est valide.
12. Le système crée le compte.
13. Le système authentifie l'utilisateur.
14. Fin de l'activité.

## Scénario alternatif
### 5 - Adresse e-mail déjà utilisée
5.1. Le système constate que l'adresse e-mail existe déjà.

5.2. Le système affiche un message indiquant que l'adresse e-mail est déjà utilisée.

5.3. Le visiteur peut saisir une autre adresse e-mail.

5.4. Reprise au point **3** du scénario nominal.

### 10 - Code OTP incorrect
10.1. Le système constate que le code OTP saisi est incorrect.

10.2. Le système affiche un message d'erreur.

10.3. Le visiteur peut saisir à nouveau le code OTP ou demander un nouveau code.

10.4. Reprise au point **9** du scénario nominal.

## Scénario exceptionnel
### 8 - Échec de l'envoi du code OTP
8.1. Le service d'envoi ne parvient pas à transmettre le code.

8.2. Le système informe le visiteur de l'échec de l'envoi.

8.3. Fin de l'activité.

---

# DA4 — S'authentifier

## Généralité
- **Activité:** « S'authentifier »
- **Acteur principal:** Utilisateur Standard
- **Acteur secondaire:** Service d'envoi du code OTP
- **Précondition:** L'utilisateur possède un compte JeryMotro et la page de connexion est accessible.
- **Début:** L'utilisateur ouvre la page de connexion.
- **Postcondition:** L'utilisateur est authentifié et accède aux fonctionnalités qui lui sont autorisées.

## Scénario nominal
1. L'utilisateur ouvre la page de connexion.
2. Le système propose les modes d'authentification disponibles.
3. L'utilisateur choisit le mode souhaité.
4. Le système demande les informations nécessaires au mode choisi.
5. L'utilisateur fournit les informations demandées.
6. Le système recherche le compte correspondant.
7. Le système vérifie les informations d'authentification.
8. Les informations sont valides.
9. Le système authentifie l'utilisateur.
10. Le système ouvre son espace utilisateur.
11. Fin de l'activité.

## Scénario alternatif
### 3 - Authentification par mot de passe
3.1. L'utilisateur choisit le mode « Mot de passe ».

3.2. Le système demande l'adresse e-mail et le mot de passe.

3.3. L'utilisateur saisit son adresse e-mail et son mot de passe.

3.4. Le système recherche le compte correspondant à l'adresse e-mail.

3.5. Le système vérifie le mot de passe.

3.6. Le mot de passe est correct.

3.7. Reprise au point **9** du scénario nominal.

### 3 - Authentification par code OTP
3.1. L'utilisateur choisit le mode « Code OTP ».

3.2. Le système propose les canaux disponibles : e-mail, SMS ou WhatsApp.

3.3. L'utilisateur choisit le canal et fournit l'adresse ou le numéro associé à son compte.

3.4. Le système recherche le compte correspondant.

3.5. Le compte existe.

3.6. Le système génère un code OTP à six chiffres.

3.7. Le système envoie le code OTP par le canal choisi.

3.8. L'utilisateur saisit le code OTP reçu.

3.9. Le système vérifie le code OTP.

3.10. Le code OTP est valide.

3.11. Reprise au point **9** du scénario nominal.

### 6 - Compte inexistant
6.1. Le système ne trouve aucun compte correspondant aux informations fournies.

6.2. Le système informe l'utilisateur qu'aucun compte JeryMotro n'est associé aux informations saisies.

6.3. L'utilisateur peut créer un compte.

6.4. Fin de l'activité.

### 7 - Informations incorrectes
7.1. Le système constate que le mot de passe ou le code OTP est incorrect.

7.2. Le système affiche un message d'erreur.

7.3. L'utilisateur peut recommencer la saisie.

7.4. Reprise au point correspondant du mode d'authentification choisi.

## Scénario exceptionnel
### 3 - Échec de l'envoi du code OTP
3.1. Le service d'envoi ne parvient pas à transmettre le code.

3.2. Le système informe l'utilisateur de l'échec de l'envoi.

3.3. Fin de l'activité.

---

# DA5 — Consulter les statistiques

## Généralité
- **Activité:** « Consulter les statistiques »
- **Acteur principal:** Utilisateur Standard
- **Précondition:** L'utilisateur est authentifié et les données nécessaires sont disponibles.
- **Début:** L'utilisateur ouvre la fonctionnalité de statistiques.
- **Postcondition:** Les statistiques disponibles sont affichées.

## Scénario nominal
1. L'utilisateur ouvre la page des statistiques.
2. Le système récupère les données nécessaires.
3. Le système traite les données disponibles.
4. Le système affiche les indicateurs statistiques.
5. L'utilisateur consulte les résultats.
6. Fin de l'activité.

## Scénario alternatif
### 2 - Données insuffisantes
2.1. Le système ne dispose pas de données suffisantes pour certains indicateurs.

2.2. Le système affiche les informations disponibles.

2.3. Fin de l'activité.

---

# DA6 — Dialoguer avec le Chat IA

## Généralité
- **Activité:** « Dialoguer avec le Chat IA »
- **Acteur principal:** Utilisateur Standard
- **Acteur secondaire:** n8n
- **Acteur secondaire:** Base de connaissances Qdrant
- **Précondition:** Le Chat IA est accessible et le service n8n peut recevoir les requêtes.
- **Début:** L'utilisateur saisit une question dans le Chat IA.
- **Postcondition:** Une réponse adaptée à la question est affichée à l'utilisateur lorsque les données nécessaires sont disponibles.

## Scénario nominal
1. L'utilisateur ouvre le Chat IA.
2. L'utilisateur saisit une question.
3. JeryMotro reçoit la question et la transmet au workflow n8n.
4. n8n reçoit la requête.
5. n8n analyse la question et identifie le type de demande.
6. n8n détermine les sources nécessaires pour construire la réponse.
7. n8n récupère les informations historiques ou les données relatives aux feux depuis la base de données JeryMotro lorsque la question concerne l'historique des feux ou les données du système.
8. n8n interroge la base de connaissances Qdrant lorsque la question concerne les connaissances générales sur les feux de brousse, notamment leur origine, leurs causes ou leur étude.
9. Lorsque la question nécessite les deux sources, n8n récupère les informations depuis la base de données JeryMotro et Qdrant.
10. n8n combine et met en contexte les informations récupérées.
11. n8n génère la réponse à partir des informations disponibles.
12. JeryMotro reçoit la réponse de n8n.
13. Le système affiche la réponse à l'utilisateur.
14. Fin de l'activité.

## Scénario alternatif
### 6 - Question nécessitant la base de données JeryMotro
6.1. n8n identifie une question portant principalement sur l'historique des feux ou sur les données enregistrées dans JeryMotro.

6.2. n8n interroge la base de données JeryMotro.

6.3. n8n utilise les résultats pour construire la réponse.

6.4. Reprise au point **10** du scénario nominal.

### 6 - Question nécessitant la base de connaissances Qdrant
6.1. n8n identifie une question portant sur les connaissances générales relatives aux feux de brousse, par exemple leur origine, leurs causes ou leur étude.

6.2. n8n interroge la base de connaissances Qdrant.

6.3. n8n utilise les résultats pour construire la réponse.

6.4. Reprise au point **10** du scénario nominal.

### 6 - Question nécessitant les deux sources
6.1. n8n identifie une question nécessitant à la fois des données JeryMotro et des connaissances générales.

6.2. n8n interroge la base de données JeryMotro.

6.3. n8n interroge la base de connaissances Qdrant.

6.4. n8n combine les informations obtenues.

6.5. Reprise au point **11** du scénario nominal.

### 7 ou 8 - Aucune information suffisante
7.1. Les sources interrogées ne fournissent pas suffisamment d'informations pour répondre correctement à la question.

7.2. n8n prépare une réponse indiquant que les informations disponibles ne permettent pas de fournir une réponse fiable.

7.3. JeryMotro affiche la réponse à l'utilisateur.

7.4. Fin de l'activité.

## Scénario exceptionnel
### 4 - Service n8n indisponible
4.1. n8n ne peut pas recevoir ou traiter la requête.

4.2. JeryMotro ne reçoit pas de réponse exploitable.

4.3. Le système informe l'utilisateur que le Chat IA est temporairement indisponible.

4.4. Fin de l'activité.

---

# DA7 — Recevoir des alertes e-mail

## Généralité
- **Activité:** « Recevoir des alertes e-mail »
- **Acteur principal:** Utilisateur Standard
- **Acteur secondaire:** Service d'envoi d'e-mails
- **Précondition:** L'utilisateur possède un abonnement d'alerte actif et le canal e-mail est configuré.
- **Début:** Une condition d'alerte correspondant aux paramètres de l'utilisateur est détectée.
- **Postcondition:** L'alerte e-mail est envoyée et son état est enregistré.

## Scénario nominal
1. Le système détecte une condition correspondant aux paramètres d'alerte.
2. Le système vérifie que l'abonnement de l'utilisateur est actif et que le canal e-mail est activé.
3. Le système prépare le message d'alerte.
4. Le système envoie le message par le service d'e-mail.
5. Le service d'envoi confirme la transmission.
6. Le système enregistre l'alerte comme envoyée.
7. Fin de l'activité.

## Scénario alternatif
### 2 - Canal e-mail non activé
2.1. Le canal e-mail n'est pas activé pour l'utilisateur.

2.2. Le système ne transmet pas l'alerte par e-mail.

2.3. Fin de l'activité.

---

# DA8 — Définir une zone prioritaire

## Généralité
- **Activité:** « Définir une zone prioritaire »
- **Acteur principal:** Utilisateur Premium
- **Précondition:** L'utilisateur est authentifié et dispose de la fonctionnalité de zone prioritaire.
- **Début:** L'utilisateur ouvre la configuration de sa zone prioritaire.
- **Postcondition:** La zone prioritaire est enregistrée dans ses préférences.

## Scénario nominal
1. L'utilisateur ouvre la gestion de sa zone prioritaire.
2. Le système affiche l'interface de sélection géographique.
3. L'utilisateur définit la zone souhaitée.
4. Le système vérifie la zone sélectionnée.
5. La zone est valide.
6. Le système enregistre la zone prioritaire.
7. Le système confirme l'enregistrement.
8. Fin de l'activité.

## Scénario alternatif
### 4 - Zone invalide
4.1. Le système détecte une zone invalide.

4.2. Le système demande à l'utilisateur de modifier la sélection.

4.3. Reprise au point **3** du scénario nominal.

---

# DA9 — Recevoir des alertes SMS et WhatsApp

## Généralité
- **Activité:** « Recevoir des alertes SMS et WhatsApp »
- **Acteur principal:** Utilisateur Premium
- **Acteur secondaire:** Services d'envoi SMS et WhatsApp
- **Précondition:** L'utilisateur Premium possède un abonnement actif et les coordonnées des canaux activés sont configurées.
- **Début:** Une condition d'alerte correspondant aux paramètres de l'utilisateur est détectée.
- **Postcondition:** Les notifications activées sont envoyées et leur état est enregistré.

## Scénario nominal
1. Le système détecte une condition correspondant aux paramètres d'alerte.
2. Le système vérifie l'abonnement et les canaux activés de l'utilisateur.
3. Le système prépare le message d'alerte.
4. Le système envoie le message par SMS et/ou WhatsApp selon les canaux configurés.
5. Les services d'envoi retournent le résultat de la transmission.
6. Le système enregistre l'état de l'alerte.
7. Fin de l'activité.

## Scénario alternatif
### 2 - Canal non disponible
2.1. Un canal SMS ou WhatsApp n'est pas activé ou ne possède pas de destination valide.

2.2. Le système utilise uniquement les canaux valides et activés.

2.3. Reprise au point **3** du scénario nominal.

---

# DA10 — Gérer les alertes

## Généralité
- **Activité:** « Gérer les alertes »
- **Acteur principal:** Utilisateur Standard ou Utilisateur Premium
- **Précondition:** L'utilisateur est authentifié.
- **Début:** L'utilisateur ouvre la gestion des alertes.
- **Postcondition:** Les préférences d'alerte sont enregistrées ou l'abonnement est désactivé selon l'action réalisée.

## Scénario nominal
1. L'utilisateur ouvre la gestion des alertes.
2. Le système charge ses préférences d'alerte.
3. L'utilisateur choisit les canaux et paramètres qu'il souhaite utiliser.
4. L'utilisateur renseigne ou modifie les coordonnées nécessaires.
5. Le système valide les informations saisies.
6. Les informations sont valides.
7. Le système crée ou met à jour l'abonnement.
8. Le système confirme l'enregistrement des préférences.
9. Fin de l'activité.

## Scénario alternatif
### 5 - Informations invalides
5.1. Le système détecte une adresse e-mail, un numéro ou un paramètre non valide.

5.2. Le système affiche une erreur.

5.3. L'utilisateur corrige les informations.

5.4. Reprise au point **4** du scénario nominal.

### 3 - Désactivation des alertes
3.1. L'utilisateur choisit de désactiver son abonnement.

3.2. Le système désactive l'abonnement.

3.3. Le système confirme la désactivation.

3.4. Fin de l'activité.

---

# DA11 — Collecter automatiquement les données FIRMS

## Généralité
- **Activité:** « Collecter automatiquement les données FIRMS »
- **Acteur principal:** NASA FIRMS
- **Précondition:** Les accès nécessaires à NASA FIRMS sont configurés et JeryMotro peut enregistrer les données collectées.
- **Début:** JeryMotro lance automatiquement une collecte de données.
- **Postcondition:** Les nouvelles détections disponibles sont intégrées dans JeryMotro et l'exécution de collecte est enregistrée.

## Scénario nominal
1. JeryMotro déclenche une collecte de données.
2. Le système interroge NASA FIRMS pour les données utilisées par JeryMotro, notamment MODIS et VIIRS.
3. NASA FIRMS retourne les données disponibles.
4. Le système analyse et prépare les données reçues.
5. Le système filtre les données nécessaires.
6. Le système supprime les doublons.
7. Le système insère ou met à jour les détections dans la base de données.
8. Le système vérifie que l'enregistrement s'est correctement déroulé.
9. Le système enregistre l'exécution et ses métriques.
10. Fin de l'activité.

## Scénario alternatif
### 2 - Une source FIRMS est indisponible
2.1. Le système détecte qu'une source FIRMS ne répond pas correctement.

2.2. Le système marque la source concernée comme indisponible ou en état dégradé.

2.3. Le système vérifie si d'autres sources disponibles permettent de poursuivre la collecte.

2.4. La collecte se poursuit avec les sources disponibles.

2.5. Reprise au point **4** du scénario nominal.

### 3 - Aucune nouvelle donnée
3.1. NASA FIRMS ne retourne aucune nouvelle donnée pour la période demandée.

3.2. Le système enregistre l'exécution sans nouvelle détection.

3.3. Fin de l'activité.

## Scénario exceptionnel
### 7 - Échec de l'enregistrement
7.1. Le système ne parvient pas à enregistrer les détections dans la base de données.

7.2. Le système enregistre l'exécution comme échouée lorsque cela est possible.

7.3. Fin de l'activité.

---

# DA12 — Générer les prédictions de risque

## Généralité
- **Activité:** « Générer les prédictions de risque »
- **Acteur principal:** Service ML externe
- **Précondition:** Les données nécessaires à la prédiction sont disponibles et le service ML externe est accessible.
- **Début:** JeryMotro transmet les données nécessaires au service ML externe.
- **Postcondition:** Les prédictions retournées par le service ML sont récupérées et disponibles pour les traitements de JeryMotro.

## Scénario nominal
1. Le système prépare les données nécessaires à la prédiction.
2. Le système transmet les données au service ML externe.
3. Le service ML externe traite les données.
4. Le service ML externe génère les prédictions de risque.
5. Le service ML externe retourne les résultats à JeryMotro.
6. Le système récupère et vérifie les résultats.
7. Le système rend les prédictions disponibles pour les traitements associés.
8. Fin de l'activité.

## Scénario alternatif
### 6 - Résultat inexploitable
6.1. Le système constate que le résultat reçu ne peut pas être exploité correctement.

6.2. Le système indique que la prédiction n'est pas disponible pour le traitement demandé.

6.3. Fin de l'activité.

## Scénario exceptionnel
### 2 - Service ML indisponible
2.1. Le service ML externe ne répond pas ou retourne une erreur.

2.2. Le système ne valide pas de nouvelle prédiction.

2.3. Fin de l'activité.

---

# DA13 — Mettre à jour le statut des feux

## Généralité
- **Activité:** « Mettre à jour le statut des feux »
- **Acteur principal:** Système JeryMotro
- **Précondition:** Des détections ou résultats de prédiction sont disponibles pour le traitement.
- **Début:** Le système lance la mise à jour des statuts à partir des nouvelles données disponibles.
- **Postcondition:** Les statuts des feux sont mis à jour dans JeryMotro.

## Scénario nominal
1. Le système récupère les nouvelles détections et les résultats nécessaires.
2. Le système regroupe les informations correspondant aux événements de feu.
3. Le système met à jour les informations temporelles des événements.
4. Le système évalue l'état de chaque feu.
5. Le système attribue le statut correspondant aux données disponibles.
6. Le système vérifie si une nouvelle activité indique la réactivation d'un feu précédemment inactif.
7. Le système enregistre les statuts mis à jour.
8. Fin de l'activité.

## Scénario alternatif
### 4 - Données insuffisantes
4.1. Le système ne dispose pas de données suffisantes pour déterminer précisément le statut.

4.2. Le système attribue le statut correspondant à l'incertitude des données lorsque nécessaire.

4.3. Le système enregistre l'état obtenu.

4.4. Fin de l'activité.

### 6 - Réactivation détectée
6.1. Le système détecte une nouvelle activité après une période sans activité.

6.2. Le système met à jour le statut du feu en conséquence.

6.3. Reprise au point **7** du scénario nominal.

---

# DA14 — Déclencher les alertes

## Généralité
- **Activité:** « Déclencher les alertes »
- **Acteur principal:** Système JeryMotro
- **Précondition:** Les événements de feu et leurs statuts sont disponibles, et les abonnements d'alerte actifs peuvent être consultés.
- **Début:** Le système détecte un événement répondant aux conditions d'alerte.
- **Postcondition:** Les alertes correspondant aux préférences des utilisateurs sont déclenchées et leur résultat est enregistré.

## Scénario nominal
1. Le système récupère les événements de feu et leurs statuts.
2. Le système identifie les événements répondant aux conditions d'alerte.
3. Le système récupère les abonnements d'alerte actifs.
4. Le système compare les caractéristiques de chaque événement avec les paramètres d'alerte des utilisateurs concernés.
5. Le système détermine les canaux de notification activés pour chaque utilisateur.
6. Le système déclenche l'envoi des alertes par les canaux correspondants.
7. Le système enregistre le résultat des notifications.
8. Fin de l'activité.

## Scénario alternatif
### 4 - Aucun utilisateur concerné
4.1. Aucun abonnement actif ne correspond aux critères de l'événement.

4.2. Le système ne déclenche aucune notification.

4.3. Fin de l'activité.

### 5 - Aucun canal valide
5.1. Un abonnement existe mais aucun canal activé ne possède une destination valide.

5.2. Le système ne transmet pas la notification à cet utilisateur.

5.3. Le système poursuit le traitement des autres utilisateurs concernés.

5.4. Fin de l'activité.

## Scénario exceptionnel
### 6 - Échec d'envoi
6.1. Un service de notification ne parvient pas à transmettre l'alerte.

6.2. Le système enregistre l'échec du canal concerné.

6.3. Le traitement se poursuit pour les autres utilisateurs ou canaux lorsque cela est possible.

6.4. Fin de l'activité.

---
