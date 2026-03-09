Représente les interactions entre objets selon un pont de vue temporel, on y met l'accent sur la chronologie des envois de message
Documente un ou plusieurs scénario d'un cas d'utilisation 
Montre:
- Les réactions du système aux actions des utilisateurs
- La création et la manipulation des objets
Utile en phase d'analyse, de conception et de tes
# Objet
Représentée par un rectangle contenant le nom de l'objet.
Syntaxe d'un objet
```
[<nomObjet>] : [<NomClasee>]
```
# Ligne de vie 
- Représente l'ensemble des opérations exécutées par un objet
- Ligne verticale pointillée dirigée vers le bas de chaque objet
- Symbolise une durée qui dépend du scénario et du comportment modélisé
![[Ligne de vie.excalidraw]]
# Barre d'activation
- Un rectangle qui remplace la ligne de vie
- Traduit l'activation de l'objet
![[Barre_d_activation]]
# Message
- Généralement un appel, un signal ou un réponse
- Représentés par des flèche horizontales reliant la ligne de vie de l'objet émetteur à la ligne de vie de l'objet récepteur
- **Message synchrone**: l'objet émetteur reste bloqué le temps lorsque l’objet récepteur traite le message envoyé
- **Message asynchrone**: l'objet émetteur n'est pas bloqué le temps lorsque l’objet récepteur traite le message envoyé
- **Message retour**
![[Message]]
- **Message de création**: un message spécifique qui donne lieu au début de la ligne de vie du nouvel objet
- **Message de destruction**: un message envoyé à un objet existant et qui donne lieu à la fin de sa ligne de vie
![[Message_de_création_Destruction]]
- **Message réflexif**: un objet envoyer un message à lui-même
- **Message récursif**: elle se présent par un déboulonnement de la barre d'activation
![[Message réflexif.excalidraw]]
# Fragments combinés
Regroupements logiques représentés par un rectangle contenant les structures conditionnelles qui affectent le flux de messages
Pour décrire les diagrammes de séquence de maniérée compacte
Définis par un opérateur et des opérandes
L'opérateur conditionne la signification du fragment combinés

Les diagrammes peuvent se référencer les un les autres:
- Poitneueur / Raccourci vers un diagramme de séquence complètement décrit
- Pour factoriser les parties de comportement à plusieurs endroits
![[Référence.excalidraw]]
![[exemble_fragemetn_combinéexcalidraw]]
## Déférents fragments combinées d'opérateur d'interaction:
> [!tip]
> ### Les opérateur des base
> - **alt**
> - **opt**
> - **loop**
> - par
> - seq
> - strict


> [!info]
> ### Opérateur pour les situations exceptionnelles
> - break


> [!hint]
> ### Opérateur pour les tests:
> - critical
> - ignore
> - consider
> - negative
> - assert

## Opérateur  "Alternative" ou *alt*
- Exprime la possibilité de choisir différents comportment
- Réalisé par le choix d'un unique opérande d'interaction en fonction des contraintes d'interaction
![[opérateur altérative alt.excalidraw]]
### Opéra "Option" ou opt:
Représente un choix dans le comportment où soit seul l'opérande d'interaction contenu dans le fragment combiné s'exécute, soit rien ne se produit
Correspond à un *alt* sans **else**
## Opérateur *loop*:
Représente un boucle
L'opérande d'interaction sera répété un certain nombre de fois