# Chat IA et RAG — architecture technique

## 1. Rôle de FastAPI

Le routeur `POST /chat` est dans `Backend/api/routers/chat.py`.

FastAPI :
1. reçoit la requête JSON du frontend ;
2. récupère l'utilisateur lorsqu'il est authentifié ;
3. vérifie les droits sur une éventuelle `zone_id` ;
4. charge le nom et le prompt personnalisé de la zone ;
5. appelle `rag_query()` ;
6. retourne une réponse normalisée.

## 2. Rôle de rag_service.py

`Backend/api/services/rag_service.py` est un client HTTP asynchrone du webhook n8n.

Il construit un payload contenant notamment :

```json
{
  "message": "...",
  "temperature": 0.1,
  "zone_id": null,
  "zone_name": null,
  "zone_prompt": null,
  "conversation_id": "...",
  "user_id": 123,
  "user_role": "standard",
  "source": "jerymotro-backend"
}
```

Les valeurs ci-dessus sont un exemple de structure, pas des données réelles.

## 3. Flux technique du Chat

```
Navigateur
   |
   | HTTPS
   v
jerymotro.duckdns.org
   |
   | requête frontend
   v
api.jerymotro.duckdns.org
   |
   | HTTP(S) JSON
   v
FastAPI /chat
   |
   | HTTP(S) POST webhook
   v
n8n
   |
   +----------------------+---------------------+
   |                      |                     |
   v                      v                     v
Base de données       Qdrant                  Modèle IA
des feux            base vectorielle       génération
   |                      |                     |
   +----------- contexte / résultats -----------+
                          |
                          v
                       n8n
                          |
                          v
                      FastAPI
                          |
                          v
                       Frontend
```

## 4. Deux types de connaissances

### A. Questions sur les données des feux

Le workflow n8n a accès à la base de données des feux.

Le rôle de cette source est de fournir des **données métier structurées et actuelles** : détections, événements et informations analytiques accessibles dans la base.

Exemples de questions :
- Combien de détections possède une région ?
- Quels événements sont actuellement visibles ?
- Quelles observations correspondent à une période donnée ?
- Quels indicateurs sont associés à une zone ?

Le principe technique est un accès aux données structurées, distinct de la recherche vectorielle.

### B. Questions nécessitant la base de connaissances

Lorsque la question nécessite des documents ou connaissances textuelles, n8n utilise Qdrant comme base vectorielle dans l'architecture déployée.

Le rôle de Qdrant est de retrouver des éléments sémantiquement proches de la question afin de fournir un contexte documentaire au modèle IA.

## 5. Pourquoi séparer SQL et Qdrant ?

La base SQL et Qdrant ne stockent pas le même type d'information :

| Système | Type de données | Usage |
|---|---|---|
| Base SQL des feux | données structurées | faits métier, filtres, agrégations |
| Qdrant | vecteurs + métadonnées documentaires | recherche sémantique / connaissance |

La séparation évite de traiter une base relationnelle comme une base vectorielle et inversement.

## 6. RAG

RAG signifie Retrieval-Augmented Generation.

Dans JeryMotro, le principe est :

```
Question
  ↓
Identification du contexte utile
  ↓
Recherche de données SQL et/ou de connaissance vectorielle
  ↓
Construction du contexte
  ↓
Modèle IA
  ↓
Réponse
```

Le détail interne des nodes n8n n'est pas stocké dans les dépôts JeryMotroBackend/JeryMotro_WEB consultés ; cette documentation décrit donc l'architecture confirmée, sans inventer les noms ou paramètres des nodes.

## 7. Qdrant

La configuration Nginx expose :

`rag.jerymotro.duckdns.org → localhost:6333`

Port 6333 = API du service Qdrant dans l'architecture documentée.

La configuration Nginx ne prouve pas le contenu exact des collections Qdrant. Elle prouve la route réseau configurée vers ce service.

## 8. Modèle IA

Le backend FastAPI ne choisit pas directement une implémentation de génération dans `rag_service.py`. Il délègue la génération au workflow n8n.

Les anciennes notes du projet mentionnent Vertex AI/Gemini comme possibilité. Ce document ne l'impose pas comme fournisseur unique sans preuve du workflow n8n actuellement exécuté.

## 9. Réponse normalisée

Le backend accepte différentes formes de sortie n8n et normalise :
- `response` ;
- `sources` ;
- `model_used` ;
- `tokens_used` ;
- `response_time_ms`.

## 10. Fallback

Si le webhook n8n est absent, indisponible ou renvoie une réponse invalide, FastAPI produit une réponse de secours.

## 11. Sécurité

Le backend transmet au workflow :
- identité utilisateur ;
- rôle ;
- zone éventuelle ;
- prompt de zone.

Une question avec `zone_id` est réservée aux rôles Premium/Admin par `chat.py`.

## 12. Résumé technique

```
Frontend
  └─ HTTPS/JSON
      └─ FastAPI /chat
          └─ HTTP(S) webhook
              └─ n8n
                  ├─ SQL / DB feux
                  ├─ Qdrant / connaissance
                  └─ modèle IA
```

> Le Chat IA n'est pas le système de détection des feux. Il exploite les données et la connaissance mises à sa disposition pour répondre aux questions.