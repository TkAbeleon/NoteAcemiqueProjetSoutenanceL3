# Fonctionnement réel

## Démarrage
Dans `Backend/api/main.py`, le backend :
1. initialise l'engine SQLAlchemy ;
2. peut lancer les migrations au démarrage ;
3. lance les checks de démarrage selon configuration ;
4. crée les tables ;
5. démarre une maintenance géographique en arrière-plan ;
6. démarre ensuite le collecteur FIRMS si activé.

## Collecte automatique
Le collecteur est une boucle asynchrone interne à FastAPI. Le code lance immédiatement `run_automatic_pipeline(collect=True)`, puis attend `collection_interval_hours`. La valeur par défaut du code est 3 h.

## Pipeline
`automatic_pipeline.py` exécute :
1. collecte FIRMS ;
2. étiquetage régional ;
3. scoring ;
4. clustering ;
5. routage automatique d'alertes candidates.

## Après collecte
Une détection est normalisée, validée géographiquement et insérée si elle est exploitable. Le backend protège les doublons par une contrainte d'unicité.

## ML
Les détections non scorées sont envoyées au service ML externe. Si le service échoue ou renvoie un score négatif, l'heuristique locale peut produire un score de repli.

## Événements
Les détections scorées et localisées sont regroupées avec HDBSCAN ou, si indisponible, avec une grille géographique.

## Statut
Le statut d'un événement dépend du temps depuis la dernière observation :
- ≤ 9 h : ACTIVE ;
- > 9 h et ≤ 24 h : COOLING ;
- > 24 h et ≤ 72 h : COOLING ;
- > 72 h : LIKELY_OUT ;
- pipeline non sain : UNKNOWN / DATA_GAP.

## Enrichissement GEE
Les scripts GEE existent séparément. `run_automatic_pipeline()` ne les appelle pas directement.

## Chat
Le frontend appelle `POST /chat`. Le backend transmet ensuite la demande au webhook n8n et normalise la réponse.

---

**Navigation :** [[01_VISION_GENERALE|← Précédent]] | [[00_INDEX|Index]] | [[03_ARCHITECTURE_TECHNIQUE|Suivant →]]
