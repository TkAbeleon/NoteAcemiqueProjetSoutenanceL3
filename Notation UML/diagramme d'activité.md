Permet de représenter le comportment interne d'un cas d’utilisation ou processus
Représente le déroulement des traitements en les regroupant dans des étapes appelées "Activité"
Prend en charge les comportment parallèles
## Nœud de bifurcation (fourche)
Création des plusieurs flots concurrents en sortie de la barre de synchronisation à partir d'un flot unique entrant
![[Nœud de bifurcation.excalidraw]]
## Nœud de jonction (synchronisation)
Production d'un flot unique sortant à partir de plusieurs flots concurrent en entrée de la synchronisation
Symétrique du nœud bifurcation
## Nœud de test-décision
Permet de faire un choix entre plusieurs flots sortant en fonction des conditions de grade de chaque flot
N'a qu'un seul flot de chaque entrée
![[Nœud de test-décision.excalidraw]]
## Nœud de fusion-test
Permet d'avoir plusieurs flots entrant possibles et un seul flot sortie
Le flot sortant est donc exécuter dès qu'un des flots entrant est activité
![[Nœud de fusion-test.excalidraw]]
## Couloir d’activités (Responsabilité)
Préciser la responsabilité de différents acteurs
Chaque activité est allouée à un couloir correspondant à la ressource concernée
![[Couloir d’activités.excalidraw]]
### Exemples de diagramme d'activité
**D-ACT1**
![[D-ACT1.jpg]]
**D-ACT2**
![[D-ACT2 1.jpg]]
