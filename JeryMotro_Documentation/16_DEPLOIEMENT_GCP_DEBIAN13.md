# Déploiement actuel — GCP Debian 13

> Le serveur de production actuel est déclaré pour le projet comme une VM Google Cloud exécutant Debian 13. Le système d'exploitation vient de l'environnement de production ; la configuration Nginx sert surtout à documenter la topologie réseau.

## Frontend
Nginx sert le build depuis :
`/mnt/jerymotro/JeryMotro_WEB/artifacts/jerymotro/dist/public`

Domaine :
`jerymotro.duckdns.org`

HTTPS est géré par Certbot.

## Backend
`api.jerymotro.duckdns.org` → `localhost:8200`

## Services visibles dans la configuration Nginx

| Domaine | Service local |
|---|---|
| api.jerymotro.duckdns.org | :8200 |
| rag.jerymotro.duckdns.org | :6333 |
| waha.jerymotro.duckdns.org | :3001 |
| chat.jerymotro.duckdns.org | :8065 |
| n8n.jerymotro.duckdns.org | :5678 |
| api.smsgate.jerymotro.duckdns.org | :3030 |
| smsgate.jerymotro.duckdns.org | :3031 |

## Rôle de Nginx
- reverse proxy ;
- terminaison TLS ;
- routage par sous-domaine ;
- support WebSocket pour certains services ;
- réglages de taille et timeouts.

## Base de données
La localisation actuelle de PostgreSQL doit être déterminée avec `DATABASE_URL`. L'ancienne documentation de déploiement parle d'un PostgreSQL local, mais cette information est historique.

## Documentation historique
`Backend/DEPLOYMENT.md` mentionne Ubuntu 22.04 et l'ancienne IP `35.192.27.164`. Ces éléments ne doivent pas être présentés comme la configuration GCP Debian 13 actuelle.

## PM2
Des scripts historiques utilisent PM2. Leur présence prouve une stratégie de déploiement existante dans le projet, pas nécessairement le gestionnaire de processus actuellement actif sur le serveur.

## Résumé
```
Internet → Nginx → Frontend / FastAPI / Qdrant / n8n / WAHA / Mattermost / SMSGate
```