# Chat IA et RAG

## Architecture réelle
`Backend/api/services/rag_service.py` est explicitement un **proxy vers n8n**.

Il ne crée pas lui-même un client ChromaDB, Qdrant ou Vertex AI.

## Flux
```
Utilisateur
   ↓
Frontend
   ↓
POST /chat
   ↓
rag_service.py
   ↓
Webhook n8n
   ↓
Workflow RAG / IA
   ↓
Réponse
```

## Contexte envoyé
Le backend transmet notamment :
- message ;
- température ;
- zone_id ;
- zone_name ;
- zone_prompt ;
- conversation_id ;
- user_id ;
- user_role ;
- source.

## Zone surveillée
Pour Premium/Admin, le backend peut charger une `MonitoredZone` et transmettre son prompt personnalisé à n8n.

## Normalisation
Le backend normalise notamment `response`, `sources`, `model_used`, `tokens_used` et `response_time_ms`.

## Fallback
Webhook absent, erreur réseau ou réponse invalide → message de secours.

## Qdrant
La configuration Nginx versionnée montre `rag.jerymotro.duckdns.org → localhost:6333`. Cela établit une brique Qdrant dans la topologie Nginx, mais ne prouve pas que chaque conversation utilise Qdrant.

## Limite
Le Chat IA n'est pas une source primaire de détection des feux.