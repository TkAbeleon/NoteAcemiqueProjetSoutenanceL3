# Nginx et architecture réseau

## 1. Rôle de Nginx

Dans JeryMotro, Nginx est la **couche d'entrée HTTP/HTTPS**. Il termine TLS, choisit le service cible en fonction du nom de domaine et transmet la requête au processus local correspondant.

Le fichier de référence est :

`UML_JeryMotro/conf.ngnix`

## 2. Ports publics et ports internes

Les clients utilisent les noms de domaine en HTTPS. Les services applicatifs écoutent ensuite sur `localhost`.

| Nom public | Cible interne | Fonction |
|---|---|---|
| `jerymotro.duckdns.org` | fichiers statiques | Frontend |
| `api.jerymotro.duckdns.org` | `localhost:8200` | FastAPI |
| `rag.jerymotro.duckdns.org` | `localhost:6333` | Qdrant |
| `waha.jerymotro.duckdns.org` | `localhost:3001` | WAHA |
| `chat.jerymotro.duckdns.org` | `localhost:8065` | Mattermost |
| `n8n.jerymotro.duckdns.org` | `localhost:5678` | n8n |
| `api.smsgate.jerymotro.duckdns.org` | `localhost:3030` | SMSGate API |
| `smsgate.jerymotro.duckdns.org` | `localhost:3031` | SMSGate Web |

## 3. Frontend

Le bloc frontend définit :

- une racine statique ;
- `index.html` ;
- des routes prerenderisées pour les pages publiques ;
- des chemins localisés `/fr`, `/mg`, `/en` ;
- un fallback SPA ;
- un cache d'un an pour `/assets/`.

Le build réel est servi depuis :

`/mnt/jerymotro/JeryMotro_WEB/artifacts/jerymotro/dist/public`

## 4. API FastAPI

La configuration :

```
api.jerymotro.duckdns.org
        ↓
http://localhost:8200
```

Nginx transmet notamment :
- Host ;
- X-Real-IP ;
- X-Forwarded-For ;
- X-Forwarded-Proto.

FastAPI peut donc connaître le contexte de la requête tout en restant non exposé directement sur Internet.

## 5. Qdrant

La configuration :

```
rag.jerymotro.duckdns.org
        ↓
http://localhost:6333
```

met à disposition l'API Qdrant.

Qdrant est utilisé dans l'architecture du Chat comme **stockage/recherche vectorielle de la base de connaissances**.

## 6. n8n

La configuration :

```
n8n.jerymotro.duckdns.org
        ↓
http://localhost:5678
```

expose n8n.

Dans le flux Chat, n8n reçoit la requête envoyée par FastAPI et orchestre ensuite :
- l'accès aux données structurées des feux ;
- l'accès à la base de connaissances via Qdrant lorsque nécessaire ;
- l'appel du modèle IA ;
- la construction de la réponse.

## 7. WAHA

```
waha.jerymotro.duckdns.org
        ↓
http://localhost:3001
```

WAHA fournit l'interface HTTP utilisée par le backend pour le canal WhatsApp.

## 8. Mattermost

```
chat.jerymotro.duckdns.org
        ↓
http://localhost:8065
```

Nginx transmet explicitement les en-têtes WebSocket et prévoit des timeouts de 600 s.

## 9. SMSGate

Deux services sont exposés :

- API : `3030`
- Web : `3031`

Le backend sélectionne SMSGate comme provider SMS lorsque `SMS_PROVIDER=smsgate`.

## 10. TLS

Les blocs HTTPS utilisent les certificats gérés par Certbot.

Le trafic :

```
Client → HTTPS/443 → Nginx → HTTP local → service
```

reste donc chiffré sur la partie publique ; les communications inter-processus montrées par `proxy_pass http://localhost:...` sont locales à l'hôte.

## 11. WebSocket et timeouts

La configuration adapte les paramètres selon les besoins des services :

- `Upgrade`
- `Connection`
- `proxy_read_timeout`
- `proxy_send_timeout`
- `proxy_connect_timeout`
- `proxy_buffering`
- `client_max_body_size`

## 12. Pourquoi cette architecture ?

Elle sépare :
- le point d'entrée public ;
- les services applicatifs ;
- les ports d'écoute internes ;
- les domaines fonctionnels.

Le client n'a donc pas besoin de connaître les ports internes de chaque service.

## 13. Ce que Nginx ne prouve pas

La configuration ne permet pas à elle seule de connaître :
- la localisation de PostgreSQL ;
- les credentials ;
- le contenu des collections Qdrant ;
- les nodes exacts du workflow n8n ;
- le modèle IA réellement choisi dans chaque workflow.

Nginx documente la **topologie réseau**, pas le détail fonctionnel de tous les traitements.
