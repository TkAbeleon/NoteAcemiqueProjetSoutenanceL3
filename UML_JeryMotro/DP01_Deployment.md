# DP01 — Diagramme de déploiement

## Position dans le projet

Le diagramme de déploiement complète les diagrammes UML du projet JeryMotro. Il décrit la répartition des composants réellement déployés et leurs communications.

> **Important :** ce diagramme est un complément d'architecture. Il ne remplace pas les diagrammes demandés dans le cours.

## Architecture réelle

JeryMotro utilise actuellement **un serveur unique** pour les principaux services applicatifs. Les services communiquent entre eux localement via `localhost` et leurs ports respectifs.

### Services principaux

| Composant | Déploiement / accès |
|---|---|
| Nginx | Reverse proxy et terminaison TLS |
| Frontend | Application Web servie par Nginx |
| Backend FastAPI | `localhost:8200` |
| PostgreSQL | Base de données du backend |
| Qdrant | `localhost:6333` |
| n8n | `localhost:5678` |
| WAHA | `localhost:3001` |
| Mattermost | `localhost:8065` |
| SMSGate | `localhost:3030`, lorsqu'il est sélectionné |
| HTTPSMS | Service SMS alternatif selon `.env` |

La configuration Nginx de travail confirme les proxys vers les services locaux du serveur, notamment le backend sur `8200`, Qdrant sur `6333`, WAHA sur `3001`, Mattermost sur `8065`, n8n sur `5678` et SMSGate sur `3030`. fileciteturn357file0L2-L2

## Communications

- Utilisateur → Nginx : HTTPS.
- Nginx → Frontend : service de l'application Web.
- Nginx → Backend : API.
- Backend → PostgreSQL : connexion locale.
- Backend → n8n : appels locaux pour les workflows concernés.
- Backend → WAHA : appels locaux pour WhatsApp.
- Backend → SMSGate : appels locaux lorsque SMSGate est choisi.
- Backend → HTTPSMS : appel au service SMS configuré lorsque HTTPSMS est choisi.
- Backend → NASA FIRMS : collecte des données externes.
- n8n → Qdrant : recherche vectorielle du Chat IA/RAG.
- n8n → PostgreSQL : consultation des données utiles au Chat IA/RAG.
- n8n → Vertex AI : génération du Chat IA lorsque ce fournisseur est utilisé dans le workflow.

## Routage Nginx

Nginx constitue le point d'entrée HTTP/HTTPS et redirige les sous-domaines vers les services locaux. Le fichier de configuration de travail est conservé dans `UML_JeryMotro/conf.ngnix`.

Principe :

**Internet → Nginx → services locaux du serveur JeryMotro**

Il ne faut donc pas représenter chaque service comme un serveur physique distinct.

## Chat IA

Le Backend n'est pas le moteur du Chat IA : il joue le rôle de proxy vers n8n.

**Utilisateur → Frontend → Backend (proxy) → n8n → PostgreSQL / Qdrant / Vertex AI → n8n → Backend → Frontend → Utilisateur**

## Notifications

- Email : n8n.
- WhatsApp : WAHA.
- SMS : HTTPSMS ou SMSGate selon la configuration `.env`.

Le choix du service SMS est donc représenté comme une alternative de configuration et non comme deux services obligatoirement utilisés en parallèle.
