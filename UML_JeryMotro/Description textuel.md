# Descriptions textuelles des cas d'utilisation — JeryMotro

Ce document décrit les cas d'utilisation présents dans le diagramme de cas d'utilisation (DCU) de JeryMotro.

Les descriptions sont basées sur le fonctionnement réel du système et restent cohérentes avec le DCU. Pour chaque cas d'utilisation, on présente la généralité, le scénario nominal et, lorsque cela est réellement utile, un scénario alternatif. Dans ce document, le scénario alternatif correspond à une reprise du scénario nominal après une condition qui demande une nouvelle tentative, une nouvelle saisie ou un nouveau choix. Il est donc présenté sous forme de boucle avec une numérotation du type `x.1`, `x.2`, `x.3`, puis une indication explicite de reprise au point concerné du scénario nominal. Un scénario exceptionnel n'est ajouté que lorsqu'un comportement exceptionnel doit être décrit pour comprendre le cas d'utilisation.

Les éléments techniques internes (base de données, services d'orchestration, fournisseurs de notification, algorithmes et autres composants) ne sont pas utilisés comme acteurs du DCU. Les détails techniques sont réservés aux diagrammes d'activité, de séquence et d'architecture.

---

# UC1 — Créer un compte

## Généralité
- **Cas d'utilisation :** « Créer un compte »
- **Acteur principal :** Visiteur
- **Précondition :** La plateforme JeryMotro est accessible.
- **Début :** Le visiteur ouvre la page de création de compte.
- **Postcondition :** Le compte est créé lorsque les informations fournies et les vérifications nécessaires sont valides.

## Scénario nominal
1. Le visiteur demande la création d'un compte.
2. Le système affiche le formulaire d'inscription.
3. Le visiteur renseigne les informations demandées.
4. Le visiteur valide le formulaire.
5. Le système vérifie les informations fournies.
6. Le système effectue la vérification nécessaire à la création du compte.
7. La vérification est valide.
8. Le système crée le compte.
9. Le système confirme la création du compte.
10. Fin du cas d'utilisation.

## Scénario alternatif
### 5 — Informations invalides ou déjà utilisées
5.1. Le système détecte un problème dans les informations fournies.

5.2. Le système indique le problème au visiteur.

5.3. Le visiteur corrige les informations.

5.4. Reprise au point **3** du scénario nominal.

---

# UC2 — S'authentifier

## Généralité
- **Cas d'utilisation :** « S'authentifier »
- **Acteur principal :** Utilisateur Standard
- **Précondition :** Le compte de l'utilisateur existe et la plateforme est accessible.
- **Début :** L'utilisateur demande une authentification.
- **Postcondition :** L'utilisateur est authentifié et peut accéder aux fonctionnalités autorisées.

## Scénario nominal
1. L'utilisateur ouvre l'espace d'authentification.
2. Le système propose les deux modes d'authentification disponibles : **par OTP** ou **par e-mail**.
3. L'utilisateur choisit le mode d'authentification.
4. Le système demande les informations nécessaires au mode choisi.
5. L'utilisateur fournit les informations demandées.
6. Le système vérifie les informations d'authentification.
7. Les informations sont valides.
8. Le système authentifie l'utilisateur.
9. L'utilisateur accède aux fonctionnalités qui lui sont autorisées.
10. Fin du cas d'utilisation.

## Scénario alternatif
### 6 — Informations ou code incorrect
6.1. Le système constate que les informations fournies ou le code OTP ne permettent pas d'authentifier l'utilisateur.

6.2. Le système indique l'échec de l'authentification.

6.3. L'utilisateur saisit à nouveau les informations nécessaires ou choisit un autre mode d'authentification.

6.4. Reprise au point **3** du scénario nominal.

---

# UC3 — Consulter la carte des feux

## Généralité
- **Cas d'utilisation :** « Consulter la carte des feux »
- **Acteur principal :** Visiteur
- **Précondition :** La plateforme est accessible.
- **Début :** Le visiteur ouvre la carte des feux.
- **Postcondition :** Les données correspondant aux critères de consultation sont affichées sur la carte.

## Scénario nominal
1. Le visiteur ouvre la carte des feux.
2. Le système affiche la carte et les données disponibles.
3. Le visiteur choisit, lorsque nécessaire, des critères de consultation ou de filtrage.
4. Le système applique les critères sélectionnés.
5. Le système affiche les détections correspondant aux critères.
6. Le visiteur consulte les informations affichées.
7. Fin du cas d'utilisation.

## Scénario alternatif
### 3 — Modification des critères de consultation
3.1. Le visiteur souhaite modifier les critères sélectionnés.

3.2. Le visiteur choisit de nouveaux critères.

3.3. Reprise au point **4** du scénario nominal.

---

# UC4 — Consulter les feux actifs

## Généralité
- **Cas d'utilisation :** « Consulter les feux actifs »
- **Acteur principal :** Visiteur
- **Précondition :** La plateforme est accessible et des données de feux sont disponibles.
- **Début :** Le visiteur demande la consultation des feux actifs.
- **Postcondition :** Les feux considérés comme actifs par le système sont affichés.

## Scénario nominal
1. Le visiteur demande l'affichage des feux actifs.
2. Le système récupère les données nécessaires.
3. Le système sélectionne les feux correspondant au statut actif.
4. Le système affiche les feux actifs.
5. Le visiteur consulte les résultats.
6. Fin du cas d'utilisation.

## Scénario alternatif
### 3 — Nouvelle consultation
3.1. Le visiteur souhaite actualiser ou modifier sa consultation.

3.2. Le visiteur demande une nouvelle consultation.

3.3. Reprise au point **1** du scénario nominal.

---

# UC5 — Consulter les statistiques

## Généralité
- **Cas d'utilisation :** « Consulter les statistiques »
- **Acteur principal :** Utilisateur Standard
- **Précondition :** L'utilisateur est authentifié.
- **Début :** L'utilisateur ouvre la page des statistiques.
- **Postcondition :** Les statistiques disponibles sont présentées à l'utilisateur.

## Scénario nominal
1. L'utilisateur ouvre la fonctionnalité de statistiques.
2. Le système récupère les données nécessaires.
3. Le système prépare les indicateurs disponibles.
4. Le système affiche les statistiques.
5. L'utilisateur consulte les résultats.
6. Fin du cas d'utilisation.

## Scénario alternatif
### 4 — Modification de la consultation
4.1. L'utilisateur souhaite consulter les statistiques selon d'autres critères disponibles.

4.2. L'utilisateur modifie sa demande de consultation.

4.3. Reprise au point **2** du scénario nominal.

---

# UC6 — Dialoguer avec le Chat IA

## Généralité
- **Cas d'utilisation :** « Dialoguer avec le Chat IA »
- **Acteur principal :** Utilisateur Standard
- **Précondition :** L'utilisateur est authentifié et le Chat IA est accessible.
- **Début :** L'utilisateur saisit une question.
- **Postcondition :** Une réponse est affichée lorsque le traitement de la demande aboutit.

## Scénario nominal
1. L'utilisateur ouvre le Chat IA.
2. L'utilisateur saisit une question.
3. Le système transmet la demande au service de Chat IA.
4. Le service traite la demande et prépare une réponse à partir des informations dont il dispose.
5. Le système reçoit la réponse.
6. Le système affiche la réponse à l'utilisateur.
7. Fin du cas d'utilisation.

## Scénario alternatif
### 2 — Nouvelle question
2.1. L'utilisateur souhaite poursuivre la conversation avec une autre question.

2.2. L'utilisateur saisit une nouvelle question.

2.3. Reprise au point **3** du scénario nominal.

---

# UC7 — Gérer les alertes

## Généralité
- **Cas d'utilisation :** « Gérer les alertes »
- **Acteur principal :** Utilisateur Standard
- **Précondition :** L'utilisateur est authentifié.
- **Début :** L'utilisateur ouvre la gestion des alertes.
- **Postcondition :** Les paramètres d'alerte sont enregistrés selon les choix effectués.

## Scénario nominal
1. L'utilisateur ouvre la gestion des alertes.
2. Le système affiche les paramètres d'alerte disponibles.
3. L'utilisateur choisit le canal d'alerte à utiliser.
4. L'utilisateur renseigne ou sélectionne la destination nécessaire au canal choisi.
5. Lorsque cela est nécessaire, le système effectue la vérification de la destination.
6. L'utilisateur active ou modifie les paramètres d'alerte.
7. Le système enregistre la configuration.
8. Le système confirme la prise en compte des paramètres.
9. Fin du cas d'utilisation.

## Scénario alternatif
### 4 — Destination invalide ou absente
4.1. La destination fournie ne peut pas être utilisée.

4.2. Le système demande une correction.

4.3. L'utilisateur corrige la destination.

4.4. Reprise au point **4** du scénario nominal.

---

# UC8 — Recevoir les alertes e-mail

## Généralité
- **Cas d'utilisation :** « Recevoir les alertes e-mail »
- **Acteur principal :** Utilisateur Standard
- **Précondition :** L'utilisateur est authentifié et a préalablement configuré et activé la réception des alertes e-mail.
- **Début :** Une condition correspondant aux paramètres d'alerte de l'utilisateur est détectée.
- **Postcondition :** Une notification e-mail est transmise lorsque les conditions de l'alerte sont satisfaites.

## Scénario nominal
1. Le système identifie une situation correspondant aux paramètres d'alerte.
2. Le système vérifie que l'alerte e-mail est configurée et active.
3. Le système prépare les informations de l'alerte.
4. Le système déclenche l'envoi de la notification e-mail.
5. La notification e-mail est transmise à l'utilisateur.
6. Fin du cas d'utilisation.

## Scénario alternatif
### 2 — Configuration de l'alerte à corriger
2.1. Le système constate que la réception e-mail n'est pas correctement configurée ou activée.

2.2. L'utilisateur ouvre la gestion des alertes.

2.3. L'utilisateur corrige ou active la configuration e-mail.

2.4. Reprise au point **2** du scénario nominal.

---

# UC9 — Recevoir les alertes SMS et WhatsApp

## Généralité
- **Cas d'utilisation :** « Recevoir les alertes SMS et WhatsApp »
- **Acteur principal :** Utilisateur Premium
- **Précondition :** L'utilisateur est authentifié, dispose de l'accès Premium et a préalablement configuré et activé le canal concerné.
- **Début :** Une condition correspondant aux paramètres d'alerte de l'utilisateur est détectée.
- **Postcondition :** La notification est transmise par le canal activé lorsque les conditions de l'alerte sont satisfaites.

## Scénario nominal
1. Le système identifie une situation correspondant aux paramètres d'alerte.
2. Le système vérifie que le canal SMS ou WhatsApp est configuré et actif.
3. Le système prépare les informations de l'alerte.
4. Le système déclenche l'envoi sur le canal configuré.
5. La notification est transmise à l'utilisateur.
6. Fin du cas d'utilisation.

## Scénario alternatif
### 2 — Configuration du canal à corriger
2.1. Le système constate que le canal concerné n'est pas correctement configuré ou activé.

2.2. L'utilisateur ouvre la gestion des alertes.

2.3. L'utilisateur corrige ou active la configuration du canal.

2.4. Reprise au point **2** du scénario nominal.

---

# UC10 — Définir une zone prioritaire

## Généralité
- **Cas d'utilisation :** « Définir une zone prioritaire »
- **Acteur principal :** Utilisateur Premium
- **Précondition :** L'utilisateur est authentifié et dispose de l'accès Premium.
- **Début :** L'utilisateur ouvre la gestion de ses zones prioritaires.
- **Postcondition :** La zone définie est enregistrée dans les paramètres de l'utilisateur.

## Scénario nominal
1. L'utilisateur ouvre la gestion des zones prioritaires.
2. Le système affiche les possibilités de définition d'une zone.
3. L'utilisateur définit la zone qu'il souhaite surveiller en priorité.
4. L'utilisateur valide la zone.
5. Le système vérifie les informations nécessaires.
6. Le système enregistre la zone prioritaire.
7. Le système confirme l'enregistrement.
8. Fin du cas d'utilisation.

## Scénario alternatif
### 5 — Zone à corriger
5.1. Les informations fournies ne permettent pas d'enregistrer correctement la zone.

5.2. Le système signale le problème.

5.3. L'utilisateur modifie la définition de la zone.

5.4. Reprise au point **3** du scénario nominal.

---

# UC11 — Exporter les données

## Généralité
- **Cas d'utilisation :** « Exporter les données »
- **Acteur principal :** Utilisateur Premium
- **Précondition :** L'utilisateur est authentifié et dispose de l'accès Premium.
- **Début :** L'utilisateur demande un export.
- **Postcondition :** Les données sélectionnées sont préparées pour être récupérées par l'utilisateur.

## Scénario nominal
1. L'utilisateur ouvre la fonctionnalité d'export.
2. Le système présente les données exportables et les options disponibles.
3. L'utilisateur choisit les données à exporter.
4. Le système prépare l'export.
5. Le système fournit le résultat de l'export à l'utilisateur.
6. Fin du cas d'utilisation.

## Scénario alternatif
### 3 — Modification de la sélection
3.1. L'utilisateur souhaite modifier les données sélectionnées pour l'export.

3.2. L'utilisateur modifie sa sélection.

3.3. Reprise au point **4** du scénario nominal.

---

# UC12 — Collecter les données

## Généralité
- **Cas d'utilisation :** « Collecter les données »
- **Acteur principal :** Administrateur
- **Précondition :** L'administrateur est authentifié, dispose des droits d'administration et la collecte peut être exécutée.
- **Début :** L'administrateur demande le lancement de la collecte.
- **Postcondition :** Les nouvelles données disponibles sont récupérées et intégrées lorsqu'elles peuvent être exploitées.

## Scénario nominal
1. L'administrateur demande le lancement de la collecte.
2. Le système démarre l'opération.
3. Le système récupère les données disponibles auprès de la source configurée.
4. Le système traite les données reçues.
5. Le système enregistre les nouvelles données exploitables.
6. Le système indique le résultat de l'opération.
7. Fin du cas d'utilisation.

## Scénario alternatif
### 3 — Nouvelle collecte
3.1. L'administrateur souhaite relancer la collecte.

3.2. L'administrateur demande une nouvelle collecte.

3.3. Reprise au point **2** du scénario nominal.

---

# UC13 — Générer les prédictions de risque

## Généralité
- **Cas d'utilisation :** « Générer les prédictions de risque »
- **Acteur principal :** Administrateur
- **Précondition :** L'administrateur est authentifié, dispose des droits d'administration et des données exploitables sont disponibles.
- **Début :** L'administrateur demande la génération des prédictions.
- **Postcondition :** Les données traitées reçoivent un résultat de risque lorsque le traitement aboutit.

## Scénario nominal
1. L'administrateur demande la génération des prédictions.
2. Le système sélectionne les données nécessaires.
3. Le système calcule ou obtient le score de risque pour les données concernées.
4. Le système associe les résultats de risque aux données traitées.
5. Le système enregistre les résultats disponibles.
6. Le système indique le résultat de l'opération.
7. Fin du cas d'utilisation.

## Scénario alternatif
### 2 — Nouvelle sélection de données
2.1. L'administrateur souhaite modifier les données à traiter.

2.2. L'administrateur relance la sélection des données exploitables.

2.3. Reprise au point **2** du scénario nominal.

---

# UC14 — Regrouper les détections

## Généralité
- **Cas d'utilisation :** « Regrouper les détections »
- **Acteur principal :** Administrateur
- **Précondition :** L'administrateur est authentifié, dispose des droits d'administration et des détections exploitables sont disponibles.
- **Début :** L'administrateur demande le regroupement des détections.
- **Postcondition :** Les détections sont regroupées lorsque les données disponibles permettent d'obtenir un résultat exploitable.

## Scénario nominal
1. L'administrateur demande le regroupement des détections.
2. Le système sélectionne les détections à traiter.
3. Le système applique le mécanisme de regroupement utilisé par JeryMotro.
4. Le système constitue les groupes de détections obtenus.
5. Le système enregistre ou met à jour les regroupements.
6. Le système indique le résultat de l'opération.
7. Fin du cas d'utilisation.

## Scénario alternatif
### 2 — Nouvelle sélection des détections
2.1. L'administrateur souhaite modifier les détections prises en compte.

2.2. L'administrateur relance la sélection des détections exploitables.

2.3. Reprise au point **2** du scénario nominal.

### Point de vigilance sur l'état actuel du projet
Le mécanisme de regroupement est implémenté dans JeryMotro. La qualité et la fiabilité du regroupement HDBSCAN nécessitent toutefois encore une consolidation avec suffisamment de données pour permettre une validation fiable.

---

# UC15 — Mettre à jour le statut des feux

## Généralité
- **Cas d'utilisation :** « Mettre à jour le statut des feux »
- **Acteur principal :** Administrateur
- **Précondition :** L'administrateur est authentifié, dispose des droits d'administration et les données nécessaires sont disponibles.
- **Début :** L'administrateur demande la mise à jour des statuts.
- **Postcondition :** Les statuts des feux traités sont mis à jour selon les informations disponibles.

## Scénario nominal
1. L'administrateur demande la mise à jour des statuts.
2. Le système récupère les informations nécessaires.
3. Le système évalue l'état des feux concernés.
4. Le système met à jour les statuts.
5. Le système enregistre les nouvelles informations.
6. Le système indique le résultat de l'opération.
7. Fin du cas d'utilisation.

## Scénario alternatif
### 2 — Nouvelle mise à jour
2.1. L'administrateur souhaite actualiser les informations prises en compte.

2.2. L'administrateur demande une nouvelle mise à jour.

2.3. Reprise au point **2** du scénario nominal.

---

# UC16 — Déclencher les alertes

## Généralité
- **Cas d'utilisation :** « Déclencher les alertes »
- **Acteur principal :** Administrateur
- **Précondition :** L'administrateur est authentifié, dispose des droits d'administration et les données nécessaires à l'évaluation des alertes sont disponibles.
- **Début :** L'administrateur demande le déclenchement des alertes.
- **Postcondition :** Les notifications correspondant aux conditions et configurations d'alerte sont déclenchées.

## Scénario nominal
1. L'administrateur demande le déclenchement des alertes.
2. Le système examine les conditions d'alerte disponibles.
3. Le système identifie les utilisateurs et canaux correspondant aux conditions remplies.
4. Le système prépare les notifications.
5. Le système déclenche les notifications correspondantes.
6. Le système indique le résultat de l'opération.
7. Fin du cas d'utilisation.

## Scénario alternatif
### 2 — Nouvelle évaluation
2.1. L'administrateur souhaite effectuer une nouvelle évaluation des conditions d'alerte.

2.2. L'administrateur demande une nouvelle évaluation.

2.3. Reprise au point **2** du scénario nominal.

---

# Relations entre cas d'utilisation

Les relations ci-dessous reprennent celles du DCU actuel.

## Authentification obligatoire

Les cas d'utilisation suivants incluent « S'authentifier » :

- `Consulter les statistiques` **<<include>>** `S'authentifier`
- `Dialoguer avec le Chat IA` **<<include>>** `S'authentifier`
- `Gérer les alertes` **<<include>>** `S'authentifier`
- `Recevoir les alertes e-mail` **<<include>>** `S'authentifier`
- `Recevoir les alertes SMS et WhatsApp` **<<include>>** `S'authentifier`
- `Définir une zone prioritaire` **<<include>>** `S'authentifier`
- `Exporter les données` **<<include>>** `S'authentifier`

## Configuration préalable des alertes

La réception d'une alerte suppose que l'utilisateur ait d'abord configuré et activé le canal concerné. Cette dépendance est représentée dans le DCU par :

- `Recevoir les alertes e-mail` **<<include>>** `Gérer les alertes`
- `Recevoir les alertes SMS et WhatsApp` **<<include>>** `Gérer les alertes`

## Généralisation des acteurs

- `Utilisateur Standard` **--|>** `Visiteur`
- `Utilisateur Premium` **--|>** `Utilisateur Standard`
- `Administrateur` **--|>** `Utilisateur Premium`

Ainsi, un acteur spécialisé hérite des cas d'utilisation de l'acteur dont il est une spécialisation.

---

# Cohérence avec le DCU

Le document reste limité aux cas d'utilisation présents dans le DCU :

- **Visiteur :** créer un compte, consulter la carte des feux, consulter les feux actifs.
- **Utilisateur Standard :** s'authentifier, consulter les statistiques, dialoguer avec le Chat IA, gérer les alertes et recevoir les alertes e-mail.
- **Utilisateur Premium :** définir une zone prioritaire, exporter les données et recevoir les alertes SMS et WhatsApp.
- **Administrateur :** collecter les données, générer les prédictions de risque, regrouper les détections, mettre à jour le statut des feux et déclencher les alertes.

Les scénarios alternatifs sont utilisés comme des boucles lorsque l'acteur doit recommencer une saisie, modifier un choix ou relancer une opération. Ils indiquent explicitement le point de reprise dans le scénario nominal. Les scénarios exceptionnels restent facultatifs et ne sont ajoutés que lorsqu'un comportement exceptionnel réel est utile à la compréhension du cas d'utilisation.
