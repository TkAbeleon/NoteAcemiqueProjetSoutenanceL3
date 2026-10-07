# Protocoles et interfaces techniques

## 1. Principe

JeryMotro est un système distribué : chaque brique possède un contrat d'interface.

```
Navigateur
   |
   | HTTPS / JSON
   v
Nginx
   |
   +--> Frontend
   |
   +--> FastAPI
           |
           +--> PostgreSQL
           +--> NASA FIRMS
           +--> ML service
           +--> n8n
           +--> WAHA
           +--> SMS
           
n8n
   +--> SQL / données feux
   +--> Qdrant
   +--> modèle IA
```

## 2. Navigateur → Nginx

**Protocole :** HTTPS  
**Port public :** 443

Nginx termine TLS puis route selon le nom d'hôte.

## 3. Frontend → Backend

Le frontend utilise des appels HTTP(S) vers la base URL API.

Le client API configuré dans `App.tsx` transmet le JWT dans :

`Authorization: Bearer <token>`

Les réponses métier sont consommées comme données JSON.

Principales familles d'interface :
- `/auth/*`
- `/detections/*`
- `/clusters/*`
- `/predictions/*`
- `/alerts/*`
- `/zones/*`
- `/chat`
- `/analytics/*`
- `/boundaries/*`
- `/regions/*`

## 4. FastAPI → PostgreSQL

**ORM :** SQLAlchemy 2.x  
**Driver :** asyncpg  
**Mode :** asynchrone

Le backend utilise un `AsyncEngine` et des sessions asynchrones.

La connexion est fournie par `DATABASE_URL`.

Le code supprime `sslmode` de l'URL avant de le traduire en paramètre SSL compatible asyncpg.

## 5. FastAPI → NASA FIRMS

**Protocole :** HTTPS  
**Format récupéré :** CSV

Le service construit des URL de l'API FIRMS avec :
- clé FIRMS ;
- source ;
- bbox ;
- nombre de jours ;
- date de début.

Les lignes sont ensuite lues par pandas.

## 6. FastAPI → microservice ML

**Protocole :** HTTP(S)  
**Client :** httpx.AsyncClient  
**Contrat :** `POST /predict`

Structure logique :

```json
{
  "instances": [...],
  "model": "xgboost-v1"
}
```

La réponse attendue contient `predictions`.

Pour chaque instance, le backend récupère notamment `risk_score` et `fire_label`.

## 7. FastAPI → n8n

**Protocole :** HTTP(S)  
**Client :** httpx.AsyncClient  
**Contrat :** webhook configuré par `N8N_CHAT_WEBHOOK_URL`.

Pour le Chat, le payload contient notamment :
- question ;
- température ;
- zone ;
- contexte utilisateur ;
- conversation_id.

Le backend ne dépend donc pas d'un SDK spécifique du moteur RAG.

## 8. n8n → base des feux

Dans l'architecture Chat de JeryMotro, n8n dispose d'un accès à la base de données relationnelle contenant les données de feux.

Cet accès permet de répondre aux questions portant sur les **données structurées du système**.

Exemples :
- détections ;
- événements ;
- périodes ;
- régions ;
- valeurs/indicateurs présents dans la base.

Le mécanisme exact des nodes SQL n'est pas documenté ici avec leurs noms internes, car ces détails ne sont pas présents dans les dépôts de code consultés.

## 9. n8n → Qdrant

Dans le workflow Chat, n8n utilise Qdrant lorsque la question nécessite des éléments provenant de la **base de connaissances**.

Qdrant fournit la recherche vectorielle/sémantique.

La route Nginx expose également :
`rag.jerymotro.duckdns.org → localhost:6333`.

## 10. n8n → modèle IA

Le workflow n8n transmet au modèle :
- la question ;
- le contexte issu de la base des feux ;
- éventuellement le contexte documentaire récupéré via Qdrant.

Le backend FastAPI ne fixe pas dans `rag_service.py` le fournisseur de génération ; celui-ci appartient au workflow n8n.

## 11. FastAPI → WAHA

**Protocole :** HTTP  
**Service :** WAHA  
**Endpoint utilisé par le backend :** `/api/sendText`

Le backend envoie notamment :
- session ;
- chatId ;
- texte.

## 12. FastAPI → SMS

Deux mécanismes sont supportés :
- HTTPSMS ;
- SMSGate.

### SMSGate
Le backend appelle :
`/3rdparty/v1/messages`

avec authentification Basic username/password.

### HTTPSMS
Le backend envoie le message au endpoint configuré avec l'API key.

## 13. Backend → Google Earth Engine

Les scripts GEE utilisent l'API Earth Engine via HTTPS/SDK.

Ils créent des géométries de points, interrogent les collections GEE et récupèrent les valeurs.

Ce traitement est séparé de l'API HTTP principale.

## 14. FastAPI → PostgreSQL local

**Protocole :** PostgreSQL / connexion SQL  
**Driver :** `asyncpg`  
**ORM :** SQLAlchemy 2.x  
**Hébergement :** PostgreSQL local sur la VM Debian 13.

Le flux est :

```text
FastAPI
   ↓
SQLAlchemy AsyncEngine
   ↓
asyncpg
   ↓
PostgreSQL local
```

Cette liaison est interne à l'infrastructure de production. Elle ne passe pas par Nginx.

## 31. Nginx → services locaux

Le reverse proxy utilise des connexions HTTP locales :

- FastAPI : 8200
- Qdrant : 6333
- WAHA : 3001
- Mattermost : 8065
- n8n : 5678
- SMSGate : 3030 / 3031

Le trafic public est donc :

`Client → HTTPS/443 → Nginx → HTTP localhost → service`

## 15. WebSockets

Nginx transmet les headers :
- `Upgrade`
- `Connection`

pour les services concernés, notamment n8n, Mattermost et les composants qui en ont besoin.

## 16. Authentification applicative

Le mécanisme frontend/backend utilise un JWT porté par le header Bearer.

Côté backend :
- `get_current_user()` impose le token ;
- `require_premium_user()` vérifie Premium/Admin ;
- `require_admin_user()` vérifie Admin.

## 17. Contrats de panne

Plusieurs interfaces possèdent un fallback.

Exemples :
- ML indisponible → score heuristique ;
- n8n indisponible → réponse Chat de secours ;
- HDBSCAN indisponible → clustering grille ;
- service SMS absent → envoi considéré échoué.

Cette stratégie réduit le couplage strict entre tous les composants.

---

**Navigation :** [[21_STACK_TECHNIQUE|← Précédent]] | [[00_INDEX|Index]] | [[23_STRATEGIE_DEPLOIEMENT_DUCKDNS|Suivant →]]
