# Nginx et accès réseau

## Référence
La configuration réseau utilisée comme référence dans les notes est :
`UML_JeryMotro/conf.ngnix`.

## Routage

| Domaine | Destination |
|---|---|
| jerymotro.duckdns.org | build frontend |
| api.jerymotro.duckdns.org | localhost:8200 |
| rag.jerymotro.duckdns.org | localhost:6333 |
| waha.jerymotro.duckdns.org | localhost:3001 |
| chat.jerymotro.duckdns.org | localhost:8065 |
| n8n.jerymotro.duckdns.org | localhost:5678 |
| api.smsgate.jerymotro.duckdns.org | localhost:3030 |
| smsgate.jerymotro.duckdns.org | localhost:3031 |

## Frontend
Nginx applique un fallback SPA et possède des routes publiques prerenderisées selon la langue.

## HTTPS
Les blocs port 443 utilisent les certificats Certbot présents dans la configuration fournie. Les blocs port 80 sont gérés par Certbot pour les domaines concernés.

## WebSockets
La configuration transmet les en-têtes Upgrade/Connection pour les services qui nécessitent des connexions persistantes.

## Pourquoi localhost ?
Les processus peuvent écouter localement tandis que Nginx fournit les noms de domaine publics et TLS.

## Ce que Nginx ne prouve pas
Le fichier ne permet pas de déduire :
- l'emplacement de PostgreSQL ;
- les valeurs des secrets ;
- le contenu de Qdrant ;
- le modèle ML réellement chargé ;
- qu'un workflow n8n est actuellement actif.

Il documente surtout la topologie d'accès.