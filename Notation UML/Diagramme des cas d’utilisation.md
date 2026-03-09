- Décrit les **fonctionnalités** d'un système  d'un point de vue utilisateurs, sous la forme d'actions et réaction
- Permet de définir les limites du système et se relation avec l'environment 
- Comprendre les **besoins de l'utilisateurs** 
- Sert à modéliser les aspect dynamique d'un système 
- Fait ressortir les acteur et les **fonction offertes par les système** 
# Système 
- Permet de délimiter le sujet de l'étude 
- Possède :
	- les cas d'utilisation 
	- mais pas les acteurs
![[Non système.excalidraw]]
# Acteur 
- Un rôles joué par une entité  extérieur au système 
- Interactions directe avec les système 
- Humain, matériel externe, autre système 
![[acteur_humain_nom_humain.excalidraw]]
- Comment identifier les acteurs?
	- Qui ont besoins les système pour réaliser le travail ?
	- Qui vont effectuer les fonction principal du système ?
	- Qui vont exécuter  les fonction principales du système (maintenance et administration )?
	- Est-ce-que que le système interagit avec le matériel ou autre système 
### Relation entre acteurs : généralisation/ spécialisation 
Dans le cas qu'un acteur peut être une spécialisation d'un autre acteur déjà défini 
![[Relation entre acteur.excalidraw]]
## Cas d'utilisation 
- Un moyen de représenter les différentes possibilité utiliser un système 
- Exprime toujours un suite d'*interaction entre acteur et l'application*
- Définit une *fonctionnalité* utilisable par un acteur 
- *Décrit par une forme verbale  (verbe à l'infinitif)*
- Comment identifier les cas d'utilisation ?
	- Qu'est ce que l'acteur attend de l'application ?
	- Quelles informations l'acteur doit-il créer, sauvegarder, consulter, modifier, détruire ?
	- Y-a-il des événement externe que l'application doit connaître .
	- Quels acteurs l'en informent?
![[Cas_d_utlisation.excalidraw]]
## Relation entre acteur et cas d'utilisation
### Relation d'association
Représente l'interaction du système avec l’extérieur
![[Relation_d_association.excalidraw]]
## Relations entre cas d'utilisation
### Relation d'inclusion (include)
Le cas d'utilisation de base en incorpore explicitement un autre, de façon *obligatoire*
![[Relation_d_inclusion]]
### Relation d'extension
Les cas d'utilisation de base en incorpore implicitement un autre, de façon *optionnelle* 
![[Relation extension]]
## Relation de généralisation/ spécialisation
Pour un cas particulier, la relation se traduit soit par la généralisation/ spécialisation
![[Relation de généralisation specification]]
## Exemples de diagramme des cas d’utilisation DCU1
![[Exemples de diagramme des cas d’utilisation DCU1]]
## [[DCU2]]
![[DCU2]]
# Description textuelle d'un cas d'utilisation
Permet de:
- clarifier le déroulement de la fonctionnalité
- décrire la chronologie des actions qui devront être réalisées
Pas normalisée par UML
Mais beaucoup d'informations à structurer
Plusieurs proposition dans la littérature

Chaque cas d’utilisation doit être décrit en détail
Commencer par les cas d’utilisation prioritaire
## Les informations à décrire
**Précondition**: quand et comment le cas d'utilisation débute
**Postcondition**: quand et comment le cas d'utilisation se termine
**Scénario nominal**: description du fonctionnement du cas d'utilisation dans les cas du scénario le plus probable
**Scénario alternatif**: description du fonctionnement du cas d'utilisation pour une partie de scénario différentes du scénario le plus probable
**Scénario exception**: description du fonctionnement du cas d'utilisation pour une partie scénario supplémentaire et optionnelle
### Exemple pour le cas d'utilisation "Payer par carte bancaire"
#### Généralité
- Acteurs principaux: Acheteur(Client, Commerçant)
- Acteurs secondaire: Système bancaire
- Précondition: L'acheteur a validé sa commende
- Début: L'acheteur arrive sur la page de paiement
- Postcondition: La commende est validée, le compte de l'entreprise est crédité
#### Scénario nominal
1. L'acheteur choisit de faire le mode paiement par carte bancaire.
2. Le système demande à l'acheteur les informations sur sa carte bancaire
3. L'acheteur saisit les informations sur sa carte bancaire
4. Les système vérifie que le numéro de carte bancaire est correct
5. Le système demande l'autorisation de prélèvement au système bancaire
6. Le système bancaire valide la transaction
7. Le système indique à l'acheteur que la commende est confirmée
#### Scénario alternatif
- 3
	- 3.1 Le numéro de la carte bancaire incorrecte
	- 3.2 L'acheteur recommence de saisir les informations sur sa carte bancaire. **Démarrage à l'étape du scénario**
- 5
	- 5.1 ...
	- 5.2 ...
#### Scénario d'exception
- 5
	- 5.1 L'acheteur annule le payement par carte bancaire
[[Diagramme de séquence]]
