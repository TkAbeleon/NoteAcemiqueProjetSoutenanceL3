---
title: Questions / réponses — MEDD
---
# Questions / réponses — Rendez-vous MEDD

## « JeryMotro, c’est quoi ? »

> « C’est un prototype de plateforme de surveillance et d’analyse des feux de végétation qui exploite notamment des données satellitaires pour produire des informations cartographiques, analytiques et des mécanismes d’alerte. »

## « Pourquoi utiliser des satellites ? »

Ils permettent d’observer de grandes surfaces et de disposer de détections sans dépendre uniquement d’une présence humaine locale.

## « Quelle est votre source de données ? »

NASA FIRMS constitue une source importante pour les détections de feux actifs. Des données complémentaires peuvent enrichir l’analyse selon les traitements disponibles.

## « L’IA détecte-t-elle le feu ? »

> « Les détections satellitaires constituent la base de l’information. L’IA intervient ensuite comme une couche d’analyse/scoring qui combine plusieurs variables. »

## « Quelle IA utilisez-vous ? »

Le microservice ML actuel du projet utilise notamment **XGBoost** pour le scoring.

## « Peut-on faire confiance au score ? »

> « Le score est un indicateur. Sa qualité doit être mesurée sur des données de validation représentatives et confrontée autant que possible aux observations de terrain. »

## « Pourquoi ne pas dire qu’un feu est éteint ? »

Parce qu’une absence de détection FIRMS n’est pas une preuve d’extinction. Des nuages, la fréquence de passage, l’intensité du feu ou des limites de collecte peuvent expliquer une absence de signal.

## « Est-ce automatique ? »

Une partie de l’architecture est conçue pour l’automatisation, notamment avec des workflows. Il faut toutefois distinguer les chaînes effectivement validées de celles encore en phase de stabilisation ou de test.

## « Est-ce déjà un outil opérationnel du ministère ? »

> « Non. C’est un prototype que je souhaite justement confronter à des besoins et données institutionnels pour évaluer une éventuelle expérimentation. »

## « Est-ce que cela remplace les agents ? »

> « Non. L’objectif est de fournir une information supplémentaire pour faciliter la surveillance et la décision. La validation et l’action restent humaines et institutionnelles. »

## « Qu’est-ce qu’il vous faudrait pour aller plus loin ? »

- validation des besoins métier ;
- données institutionnelles pertinentes ;
- observations de terrain pour l’évaluation ;
- définition d’une zone pilote ;
- critères de performance ;
- validation de l’infrastructure et de la sécurité ;
- tests en conditions réelles.

## « Quel est le principal défi ? »

> « La qualité et la disponibilité des données. Un modèle peut être techniquement correct, mais sa valeur dépend fortement de la qualité des données utilisées pour l’entraînement, la validation et l’exploitation. »

## « Quel est le rôle du Chat IA ? »

> « Il fournit une interface conversationnelle pour interroger les informations disponibles. Le workflow est orchestré par n8n ; le backend joue notamment le rôle de passerelle. »

## « Pourquoi avoir plusieurs canaux d’alerte ? »

Parce que les utilisateurs n’ont pas tous les mêmes moyens de communication. Le système prévoit notamment email, SMS et WhatsApp, sous réserve de la configuration et de la validation des intégrations.

## « Quel serait le premier pilote intéressant ? »

Ne pas choisir arbitrairement une région. Demander au MEDD quelle zone et quel cas d’usage disposent déjà de données et d’observations permettant une évaluation sérieuse.
