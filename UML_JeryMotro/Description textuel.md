# Cas d'utilisation

## Généralité:
- **Cas d'utilisation:** « S'authentifier »
- **Acteur principal:** Utilisateur
- **Acteur secondaire:** Service d'envoi du code OTP
- **Précondition:** L'utilisateur possède un compte JeryMotro et la page de connexion est ouverte.
- **Début:** L'utilisateur choisit de se connecter à son compte.
- **Postcondition:** L'utilisateur est authentifié et accède aux fonctionnalités autorisées de JeryMotro.

## Scénario nominal:
1. L'utilisateur ouvre la page de connexion.
2. Le système propose les modes d'authentification disponibles: mot de passe ou code OTP.
3. L'utilisateur choisit un mode d'authentification.
4. Le système demande les informations nécessaires au mode choisi.
5. L'utilisateur fournit les informations demandées.
6. Le système vérifie les informations d'authentification.
7. Les informations sont valides.
8. Le système authentifie l'utilisateur.
9. Le système ouvre l'espace utilisateur.
10. L'utilisateur accède aux fonctionnalités autorisées de JeryMotro.

## Scénario alternatif:

### 4 - Connexion par mot de passe
4.1. L'utilisateur choisit le mode « Mot de passe ».

4.2. Le système demande l'adresse e-mail et le mot de passe.

4.3. L'utilisateur saisit son adresse e-mail et son mot de passe.

4.4. Le système recherche le compte correspondant à l'adresse e-mail.

4.5. Le système vérifie le mot de passe.

4.6. Les informations sont correctes.

4.7. Le système authentifie l'utilisateur.

4.8. Reprise au point **9** du scénario nominal.

### 4 - Connexion par code OTP
4.1. L'utilisateur choisit le mode « Code OTP ».

4.2. Le système propose le canal d'envoi du code OTP: e-mail, SMS ou WhatsApp.

4.3. L'utilisateur choisit le canal et fournit l'adresse e-mail ou le numéro associé à son compte.

4.4. Le système recherche le compte correspondant.

4.5. Le système génère un code OTP à six chiffres.

4.6. Le système envoie le code OTP par le canal choisi.

4.7. L'utilisateur saisit le code OTP reçu.

4.8. Le système vérifie le code OTP.

4.9. Le code OTP est valide.

4.10. Le système authentifie l'utilisateur.

4.11. Reprise au point **9** du scénario nominal.

## Scénario alternatif:

### 4.4 - Compte inexistant
4.4.1. Le système ne trouve aucun compte correspondant aux informations fournies.

4.4.2. Le système informe l'utilisateur qu'aucun compte JeryMotro n'est associé aux informations saisies.

4.4.3. Le système invite l'utilisateur à créer un compte.

4.4.4. Fin du cas d'utilisation.

### 4.5 - Mot de passe incorrect
4.5.1. Le système constate que le mot de passe saisi est incorrect.

4.5.2. Le système affiche un message d'erreur.

4.5.3. L'utilisateur peut saisir à nouveau ses informations de connexion.

4.5.4. Reprise au point **4.3** du scénario « Connexion par mot de passe ».

### 4.8 - Code OTP incorrect
4.8.1. Le système constate que le code OTP saisi est incorrect.

4.8.2. Le système affiche un message d'erreur.

4.8.3. L'utilisateur peut saisir à nouveau le code OTP.

4.8.4. Reprise au point **4.7** du scénario « Connexion par code OTP ».

### 4.6 - Demande d'un nouveau code OTP
4.6.1. L'utilisateur demande un nouveau code OTP.

4.6.2. Le système génère un nouveau code OTP.

4.6.3. Le système envoie le nouveau code OTP par le canal choisi.

4.6.4. Reprise au point **4.7** du scénario « Connexion par code OTP ».

## Scénario exception:

### 4.6 - Échec de l'envoi du code OTP
4.6.1. Le service d'envoi OTP ne parvient pas à transmettre le code.

4.6.2. Le système informe l'utilisateur que l'envoi du code a échoué.

4.6.3. L'utilisateur peut demander un nouvel envoi ou quitter la procédure.

4.6.4. Fin du cas d'utilisation.

### 4.8 - Code OTP expiré
4.8.1. Le système constate que le code OTP est expiré.

4.8.2. Le système informe l'utilisateur que le code OTP n'est plus valide.

4.8.3. L'utilisateur demande un nouveau code OTP.

4.8.4. Reprise au point **4.6** du scénario « Connexion par code OTP ».

### 6 - Compte désactivé
6.1. Le système détecte que le compte correspondant est désactivé.

6.2. Le système refuse l'authentification.

6.3. Le système informe l'utilisateur que le compte n'est pas actif.

6.4. Fin du cas d'utilisation.

-------
# Cas d'utilisation "Créer compte"
## Généralité:
- Cas d'utilisation "Créer compte"
- Acteur: Visiteur
- Précondition: Page de création de compte ouvert
## Scénario nominal:
1. L'utilisateur remplit le formulaire d'inscription(Nom, email, organisation, mot de passe)
2. L'utilisateur valide
3. Le système recherche si l'email est unique
4. Le système envoi un code OTP à 6 chiffre par email vers l’utilisateur
5. L'utilisateur saisi le code OTP
6. Compte créé et utilisateur connecté
## Scénario alternatif:
3. Le système recherche si l'email est unique
	- 3.1  L’adresse email existe déjà.
	3.2 Le système affiche une erreur de duplication. Reprise au point *1.*
4. L'utilisateur saisi le code OTP
   - 4.1 Code OTP invalide
   - 4.2 Le système affiche une erreur. Reprise au point *5.* ou l’utilisateur demande un nouveau code OTP et reprise au point *4.*
----
