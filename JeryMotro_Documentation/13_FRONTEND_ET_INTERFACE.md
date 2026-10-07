# Frontend et interface Web

## Technologie
Le dépôt JeryMotro_WEB est une application React/Vite. Le code utilise notamment React Query, Wouter, l'authentification, le thème et l'i18n.

## Espaces fonctionnels
L'application contient notamment :
landing, login, register, map, dashboard, detections, clusters, predictions, stats, chat, zones, alerts, profile, export, access-request et administration.

## Carte
La carte active utilise Leaflet / react-leaflet et consomme principalement les détections de l'API.

Les filtres observés comprennent notamment période, région, source et risque.

## API cartographique
Le backend possède aussi une nouvelle API analytics :
- `/analytics/v1/map/config`
- `/geojson/{mode}`
- `/features/{feature_type}/{feature_id}`

Le code frontend de carte active observé n'est pas démontré comme reposant entièrement sur cette nouvelle API.

## Dashboard et statistiques
Le dashboard présente des indicateurs de détections, risque, environnement et événements. La page Stats consomme les routes statistiques avancées.

Une valeur d'accuracy affichée dans le frontend ne constitue pas, à elle seule, une métrique scientifique calculée dynamiquement.

## Export
La page Export prépare côté frontend des sorties CSV/JSON/PDF à partir des données récupérées.

## Internationalisation
Le projet prend en charge français, malgache et anglais dans les interfaces concernées.

## Authentification côté client
Le frontend conserve le JWT et les informations utilisateur dans localStorage et vérifie notamment l'expiration côté client. L'autorisation finale reste du ressort du backend.