# Cas d'utilisation
## Généralité:
- Cas d'utilisation
- Acteur:
- Précondition:
## Scénario nominal:
## Scénario alternatif:
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
# Cas d'utilisation:"S'authentifier"
## Généralité:
- Cas d'utilisation "S'authentifier"
- Acteur: Utilisateur standard
- Précondition:Page de connexion ouvert
## Scénario nominal:
1. L'utilisateur choisit le mode de connexion par code OTP ou par mot de passe
2. L'utilisateur saisi le formulaire:email et mot de passe pour connexion par mot de passe et code OTP pour la connexion par code OTP
3. Le système recherche s'il le email et le mot de passe, ou le 
## Scénario alternatif:
---
