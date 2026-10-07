# Architecture technique

```
Utilisateur
   |
HTTPS
   v
Nginx
   +--> Frontend React/Vite
   +--> Backend FastAPI :8200
             |
             +--> Base SQL
             +--> NASA FIRMS
             +--> Service ML
             +--> n8n
             +--> WAHA
             +--> SMS
```

## Frontend
React/Vite, Wouter, React Query, authentification, thème et i18n. L'interface comporte carte, dashboard, détections, clusters, statistiques, prédictions, chat, zones, alertes et export.

## Backend
FastAPI charge notamment les routers access_requests, admin_users, alerts, analytics, auth, boundaries, chat, clusters, detections, internal, predictions, regions et zones.

## Persistance
SQLAlchemy async est utilisé pour les modèles métier, notamment utilisateurs, détections FIRMS, événements de feu, alertes, abonnements, zones et prédictions.

## Géographie
Le code précise que la géométrie régionale est calculée côté Python avec GeoJSON + Shapely ; il ne faut pas représenter Layerbase comme fournissant PostGIS pour cette fonction.

## Services externes
NASA FIRMS fournit les observations. Le service ML calcule le scoring. n8n orchestre les workflows et le Chat. WAHA gère WhatsApp. Les fournisseurs SMS sont configurables. Nginx fait le reverse proxy et termine TLS.

## UML
NASA FIRMS, n8n, Qdrant, service ML, WAHA et fournisseurs SMS sont des composants techniques externes, pas des classes métier SQLAlchemy.