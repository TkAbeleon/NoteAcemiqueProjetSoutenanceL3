# Descriptions textuelles des cas d'utilisation — JeryMotro

Ce document décrit les cas d'utilisation présents dans le diagramme de cas d'utilisation (DCU) de JeryMotro.

Les descriptions sont basées sur le fonctionnement réel du système et restent cohérentes avec le DCU. Pour chaque cas d'utilisation, on présente la généralité, le scénario nominal et, lorsque cela est réellement utile, un scénario alternatif. Un scénario exceptionnel n'est ajouté que lorsqu'un comportement exceptionnel doit être décrit pour comprendre le cas d'utilisation.

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
2. Le système demande les informations nécessaires.
3. L'utilisateur fournit les informations demandées.
4. Le système vérifie les informations d'authentification.
5. Les informations sont valides.
6. Le système authentifie l'utilisateur.
7. L'utilisateur accède aux fonctionnalités qui lui sont autorisées.
8. Fin du cas d'utilisation.

## Scénario alternatif
### 4 — Informations incorrectes
4.1. Les informations fournies ne permettent pas d'authentifier l'utilisateur.

4.2. Le système indique l'échec de l'authentification.

4.3. L'utilisateur peut recommencer l'authentification.

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
### 5 — Aucun résultat
5.1. Aucune détection ne correspond aux critères sélectionnés.

5.2. Le système indique qu'aucun résultat correspondant n'est disponible.

5.3. Le visiteur peut modifier les critères.

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
### 3 — Aucun feu actif
3.1. Aucun feu ne correspond au statut actif.

3.2. Le système indique qu'aucun feu actif n'est disponible.

3.3. Fin du cas d'utilisation.

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
### 2 — Données insuffisantes
2.1. Certaines données nécessaires à un indicateur ne sont pas disponibles.

2.2. Le système présente uniquement les informations disponibles.

2.3. Fin du cas d'utilisation.

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
### 4 — Informations insuffisantes
4.1. Les informations disponibles ne permettent pas de produire une réponse satisfaisante.

4.2. Une réponse indiquant cette limitation est préparée.

4.3. Le système affiche la réponse.

4.4. Fin du cas d'utilisation.

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
### 2 — Alerte e-mail non configurée ou inactive
2.1. L'utilisateur n'a pas configuré ou activé la réception des alertes e-mail.

2.2. Le système ne transmet pas la notification par e-mail.

2.3. Fin du cas d'utilisation.

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
### 2 — Canal non configuré ou inactif
2.1. Le canal choisi n'est pas configuré ou n'est pas actif.

2.2. Le système ne transmet pas la notification par ce canal.

2.3. Fin du cas d'utilisation.

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
### 5 — Zone invalide
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
### 4 — Aucune donnée à exporter
4.1. Les critères sélectionnés ne donnent aucun résultat exportable.

4.2. Le système informe l'utilisateur qu'aucune donnée n'est disponible pour l'export demandé.

4.3. Fin du cas d'utilisation.

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
### 3 — Aucune nouvelle donnée disponible
3.1. La source ne fournit aucune nouvelle donnée exploitable.

3.2. Le système termine la collecte sans ajout de nouvelles données.

3.3. Le système indique le résultat à l'administrateur.

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
### 2 — Données insuffisantes
2.1. Les données disponibles ne sont pas suffisantes pour certaines entrées.

2.2. Le système traite les données qui restent exploitables.

2.3. Le système indique le résultat obtenu.

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
### 3 — Données insuffisantes pour un regroupement exploitable
3.1. Les données disponibles ne permettent pas d'obtenir un regroupement suffisamment exploitable.

3.2. Le système indique que le résultat du regroupement est limité ou insuffisant.

3.3. Fin du cas d'utilisation.

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
### 2 — Données insuffisantes
2.1. Certaines données nécessaires ne sont pas disponibles.

2.2. Le système traite uniquement les feux pour lesquels une mise à jour est possible.

2.3. Le système indique le résultat obtenu.

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
### 3 — Aucune alerte à déclencher
3.1. Aucune condition d'alerte active ne correspond aux données traitées.

3.2. Le système ne déclenche aucune notification.

3.3. Le système indique qu'aucune alerte n'a été déclenchée.

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

Les scénarios exceptionnels ne sont pas systématiques : ils sont ajoutés uniquement lorsqu'un comportement exceptionnel réel apporte une information utile à la compréhension du cas d'utilisation.
