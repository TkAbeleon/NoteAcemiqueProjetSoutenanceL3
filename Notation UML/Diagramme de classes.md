- Diagramme **pivot** de l'ensemble de la modélisation de d'un système
- Permet de donner la représentation statique du système à développer
- Fond" sur:
	- le concept d'objet
	- le concept de classe comprenant les attributs et les opérations
	- les différents types d'association entre classes
# Classe, attribut et opération
## Classe
Décrire un groupe d'objets
Rectangle comportant plusierus compartiment:
- Compartiment 1 : nom de la classe
- Compartiment  2: attributs
- Compartiment 3: opérations
Différents niveaux de détail possible: possiblité d'omettre des attributs et/ou des opérations
![[Classe.excalidraw]]
### Attribut
Propriété élémentaire d'un classe
Attributs dérivés précédés de *"/"*

![[Attribut.excalidraw]]
### Opération
Fonction applicable aux objets d'une classe
Décrire le comportment d'un objet
Possibilité de surcharger une opération: même nom, mais paramètres différent
![[Opération.excalidraw]]
## Visibilité des attributs et opérations
*Public (+)*: Attribut ou opération visible par tous
*Privé (-)*: Attribut ou opération seulement visible à l’intérieur de la classe
*Protégé (#)*: Attribut ou opération visible seulement l’intérieur de la classe pour les toutes les sous-classe
*Paquetage (~)*: Attribut ou opération ou classe seulement visible l’intérieur du paquetage où se trouve la classe
![[Visibilité des attributs et opérationsexcalidraw]]
## Association, multiplicité
### Association
Représente les liens existants entre les instances des classes
Porte un nom (signification)
![[Association.excalidraw]]
#### Rôle d'association
Précise le rôle d'une classe au sein de l'association
Explicite le nom de l'association si besoin
![[Rôle d'association.excalidraw]]
### Multiplicité
Indique un domaine de valeurs pour préciser le nombre d'instance d'une classe vis-à-vis d'une autre classe pour une association donnée.

|       |                              
| ----- | ----------------------------- |
| 1     | un et un seul                 |
| 0...1 | zéro ou un                    |
| M...N | de M à N (entiers naturels)   |
| *     | de zéro à plusieurs           |
| 0...* | de zéro à plusieurs           |
| 1...* | de un à plusieurs             |
| N     | exactement N (entier naturel) |
**Exemple**
![[Multiplicité.excalidraw]]
### Association réflexive
Définit les liens entre des objets d'une même classe
![[Association réflexive.excalidraw]]
### Classe-association
Permet de décrire soit des attributs soit des opérations propres à l'association
![[Classe-association.excalidraw]]
### Association n-aire
Association reliant plus de deux classe
![[Association n-aire.excalidraw]]
## Agrégation et composition
### Agrégation
Pas besoin d'être nommées: *"contient"* , *"est composée de"*
Durées de vie indépendantes des objets
![[Agrégation.excalidraw]]
### Composition
Besoin d'être nommées:*"contient"* , *"est composée de"*
Durées de vie liées composants/composé
![[Composition.excalidraw]]
## Généralisation et spécialisation
Elles sont des points de vue portées sur les hierarchies de classe
### Généralisation
Consiste à factoriser dans une classe, appelée superclasse, les attributs et/ou opérations des classes considérées
### Spécialisation
Représente la démarche inverse de la généralisation
Consiste à créer à partir d'une classe, plusieurs classes spécialisées
Chaque nouvelle classe créée est dite spécialisées puisqu'elle comporte en plus des attributs ou opérations de la super-classe (disponibles par heritages) des attributs ou opérations qui lui sont propres.
![[Généralisation et spécialisation.excalidraw]]
### Héritage multiple
Une classe peut hériter des plusieurs super-classes
![[Héritage.excalidraw]]
## Association qualifiée, dépendance
### Qualification
Relation entre deux classes permettant de préciser le sémantique de l'association et de qualifier de manière restrictive les liens entre les instance
![[Qualification.excalidraw]]
### Dépendance
Permet de représenter l'existence d'un lien sémantique
Une classe Best en dépendance de la classe A si des éléments de la classe A sont nécessaires pour construire la classe B.
![[Dépendance.excalidraw]]
**Exemple**
![[Exemple_Classe.excalidraw]]
![[D Classe 1.jpg]]
![[D Classe 2.jpg|316]]
[[Exercice UML]]
