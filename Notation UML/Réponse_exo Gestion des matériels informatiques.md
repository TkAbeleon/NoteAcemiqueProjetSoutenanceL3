1. kk
2. A
3. L'agent saisi le login et le mot de passe
4. Le système accepte l'accées
5. Le système affiche le menu de l'application
### Scénario alternatif:
3.1
3.1 Les informations saisi sont incorrecte
3.4 Le système affiche la page de connexion et attends que l'utilisateurs saisisse ces informations d'authentification. **Reprise** au au point 2.
## Cas utilisation n° 2 "Faire affectation"
**Généralité** : faire affectation agent informatique:
**Précondition**: matériel à la disposition de l'utilisateurs et application active
### Scénario nominal
1. Inclusion de cas d’utilisation de authentifier
2. Le système affiche le formulaire de saisi
3. L'agent recherche le matériel dans la base donnée
4. Le système affiche les référence du matériel et de son utilisateurs
5. L'agent valide l'affectation
### Scénario allitératif
5.
5.1 Le matériel a changer d'utilisateur et/ou de destination
5.2 Le système affiche les référence de l'appareil et son utilisateurs. Reprise au point 4
## Cas d’utilisation n°3 "Demander intervention"
**Généralité**: cas d’utilisation Demander intervention
**Précondition**: arrivé de nouvel demande, application active
### Scénario nominal
1. L'utilisateurs demande autorisation à l'agent
2. Inclusion du cas d'utilisation authentifier
3. Le système affiche le formulaire de saisi
4. L'utilisateurs saisi les information sur la demande
5. utilisateurs valide la saisi
## Cas d'utilisation n°4 "traiter incident"
**Acteur**:agent informatique
**Précondition**: Application active, demande effectuer un utilisateurs
### Scénario nominal
1. Le système affiche le formulaire de saisi
2. L'agent saisi les informations sur l'incident
3. L'agent résout  le problème
4. L'agent enregistre la procedure de résolution
## Cas d'utilisation n°5 "Consulter base de donnée"
**Généralité**: Cas d'utilisation base de donnée
**Acteur**:Agent informatique
**Précondition** Application active, demande effectuer par un utilisateurs
### Scénario nominal:
1. Le système affiche le formulaire
2. L'agent clique un lien ou un bouton
3. Le système affiche les informations qui correspondent au lien ou au bouton cliqué
### Scénario allitératif
3.
3.1 L'agent ne trouve pas l'information dans la base de donné
3.2 L'agent clique sur un lien ou un bouton. **Reprise** au point 2
# Diagramme de séquence
## Diagramme de séquence pour CU n°1: "Authentifier"
## Diagramme de séquence pour CU n°2: "Faire affectation"
## Diagramme de séquence pour CU n°3: "Demander intervention"
![[Pasted image 20260326133641.png]]
## Diagramme de séquence pour CU n°4: "Traiter incident"
![[Pasted image 20260326133918.png]]
## Diagramme de séquence pour CU n°4: "Consulter base de donnée"

![[Pasted image 20260326133855.png]]
# Diagramme d'activité
## Diagramme d'activité pour CU n°1: "Authentifier"
![[Pasted image 20260326134905.png]]
## Diagramme d'activité pour CU n°2: "Faire affectation"
![[Pasted image 20260326135535.png]]
## Diagramme d'activité pour CU n°3: "Demander intervention"
![[Pasted image 20260326140024.png]]
## Diagramme de séquence pour CU n°4: "Traiter incident"
![[Pasted image 20260326141452.png]]
## Diagramme de séquence pour CU n°4: "Consulter base de donnée"
![[Pasted image 20260326141314.png]]
# Diagramme de classe
