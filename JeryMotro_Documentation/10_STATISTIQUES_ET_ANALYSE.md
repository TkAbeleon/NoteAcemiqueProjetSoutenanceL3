# Statistiques et analyse

## Routes
Le backend expose notamment des statistiques environnementales et une analyse avancée via :
`GET /detections/stats/environment/advanced`.

## Bibliothèques
L'analyse avancée utilise pandas et numpy.

## Filtres
Elle prend en charge des filtres temporels et la possibilité d'exclure le bruit.

## Indicateurs
Selon les structures de réponse utilisées par le frontend, on trouve notamment :
- moyenne, médiane ;
- variance, écart-type ;
- quartiles, IQR ;
- outliers ;
- valeurs manquantes ;
- composition de contexte ;
- corrélations de Pearson ;
- covariance ;
- statistiques clusters/événements ;
- informations géographiques.

## NULL
Les valeurs absentes doivent rester absentes. Elles ne doivent pas être assimilées à zéro. Les corrélations doivent utiliser des paires valides.

## Interprétation
Une corrélation ne prouve pas une causalité.

## Utilité
La plateforme ne se limite donc pas à une carte : les données peuvent être étudiées quantitativement.

---

**Navigation :** [[09_ENRICHISSEMENT_GEE_ENVIRONNEMENT|← Précédent]] | [[00_INDEX|Index]] | [[11_ALERTES_ET_NOTIFICATIONS|Suivant →]]
