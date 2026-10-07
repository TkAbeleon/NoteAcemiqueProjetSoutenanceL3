# Déploiement actuel — GCP Debian 13

> Le serveur de production actuel est une VM Google Cloud exécutant Debian 13. Cette information vient de l'environnement de production du projet. La configuration `UML_JeryMotro/conf.ngnix` sert de référence pour la topologie réseau.

## 1. Vue physique/logique

```
Internet
   |
   | HTTPS :443
   v
VM Google Cloud
Debian 13
   |
   v
Nginx
   |
   +--> Frontend
   +--> FastAPI :8200
   +--> Qdrant :6333
   +--> WAHA :3001
   +--> Mattermost :8065
   +--> n8n :5678
   +--> SMSGate :3030/:3031
```

La topologie ci-dessus suit les destinations locales réellement écrites dans `conf.ngnix`.

## 2. Frontend

Domaine :
`jerymotro.duckdns.org`

Racine Nginx :
`/mnt/jerymotro/JeryMotro_WEB/artifacts/jerymotro/dist/public`

La configuration contient :
- `index index.html` ;
- fallback SPA ;
- routes publiques prerenderisées ;
- variantes fr/mg/en ;
- cache long pour `/assets/` ;
- certificat TLS Certbot.

## 3. API FastAPI

Domaine :
`api.jerymotro.duckdns.org`

Proxy :
`http://localhost:8200`

FastAPI/Uvicorn écoute avec la configuration de `api.config.settings`, dont la valeur de port par défaut est 8200.

## 4. Qdrant

Domaine :
`rag.jerymotro.duckdns.org`

Proxy :
`http://localhost:6333`

Qdrant joue le rôle de **base vectorielle de la connaissance du Chat** dans l'architecture déployée.

Il est distinct de la base SQL des détections.

## 5. n8n

Domaine :
`n8n.jerymotro.duckdns.org`

Proxy :
`http://localhost:5678`

n8n est la couche d'orchestration du Chat et de plusieurs workflows d'intégration.

Dans le workflow Chat confirmé pour le projet :
- n8n peut accéder à la base de données des feux pour les questions de données métier ;
- n8n utilise Qdrant pour les questions nécessitant la base de connaissances ;
- n8n transmet le contexte utile au modèle IA puis renvoie le résultat à FastAPI.

## 6. WAHA

Domaine :
`waha.jerymotro.duckdns.org`

Proxy :
`http://localhost:3001`

Le backend utilise WAHA pour le canal WhatsApp lorsque le provider est disponible/configuré.

## 7. Mattermost

Domaine :
`chat.jerymotro.duckdns.org`

Proxy :
`http://localhost:8065`

Nginx configure explicitement les WebSockets et des timeouts de 600 s.

## 8. SMSGate

API :
`api.smsgate.jerymotro.duckdns.org → localhost:3030`

Web :
`smsgate.jerymotro.duckdns.org → localhost:3031`

Le backend peut sélectionner SMSGate comme provider SMS.

## 9. TLS et reverse proxy

Les blocs `listen 443 ssl` utilisent les certificats Certbot.

Les en-têtes de reverse proxy transmettent notamment :
- Host ;
- X-Real-IP ;
- X-Forwarded-For ;
- X-Forwarded-Proto.

Nginx gère aussi les en-têtes Upgrade/Connection lorsque les services requièrent WebSocket.

## 10. Limites de cette preuve

Nginx permet de connaître la topologie HTTP/HTTPS et les ports configurés. Il ne permet pas à lui seul de connaître :
- le contenu de PostgreSQL ;
- les collections Qdrant ;
- les credentials ;
- le modèle IA effectivement sélectionné dans chaque workflow n8n.

## 11. Base de données

Le backend utilise `DATABASE_URL` pour déterminer la cible de PostgreSQL.

L'ancienne documentation `Backend/DEPLOYMENT.md` décrit une architecture Ubuntu 22.04 avec PostgreSQL local et l'ancienne IP `35.192.27.164`. Elle est classée historique et ne remplace pas la configuration actuelle du GCP Debian 13.

## 12. Résumé réseau

| Domaine | Port local | Rôle |
|---|---:|---|
| jerymotro.duckdns.org | fichiers statiques | Frontend |
| api.jerymotro.duckdns.org | 8200 | FastAPI |
| rag.jerymotro.duckdns.org | 6333 | Qdrant |
| waha.jerymotro.duckdns.org | 3001 | WAHA |
| chat.jerymotro.duckdns.org | 8065 | Mattermost |
| n8n.jerymotro.duckdns.org | 5678 | n8n |
| api.smsgate.jerymotro.duckdns.org | 3030 | SMSGate API |
| smsgate.jerymotro.duckdns.org | 3031 | SMSGate Web |

## 13. Processus

```
Client
  ↓ HTTPS
Nginx
  ↓ reverse proxy
Service local
  ↓
traitement / accès données
```

L'architecture garde donc un point d'entrée public unique au niveau HTTP(S), malgré plusieurs processus locaux.