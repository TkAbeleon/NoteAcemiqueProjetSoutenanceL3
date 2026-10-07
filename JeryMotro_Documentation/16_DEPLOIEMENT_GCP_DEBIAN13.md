# Déploiement GCP Debian 13 — référence DuckDNS

> **Architecture retenue pour cette documentation : GCP + Debian 13 + Nginx + DuckDNS.**
>
> Le domaine de référence est **`jerymotro.duckdns.org`**. Les autres chaînes de publication présentes dans certains fichiers du frontend ne remplacent pas cette architecture dans cette documentation.

## 1. Vue d'ensemble

La VM GCP héberge les services JeryMotro et utilise Nginx comme point d'entrée HTTP/HTTPS.

```
Internet
   |
HTTPS :443
   |
   v
Nginx
   |
   +--> Frontend statique pré-rendu
   +--> FastAPI :8200
   +--> Qdrant :6333
   +--> n8n :5678
   +--> WAHA :3001
   +--> Mattermost :8065
   +--> SMSGate :3030 / :3031
```

Le système d'exploitation de production est Debian 13.

## 2. Frontend statique

Le build final est servi depuis :

```
/mnt/jerymotro/JeryMotro_WEB/artifacts/jerymotro/dist/public
```

Nginx ne compile pas React. La compilation est réalisée avant la mise en production.

Chaîne :

```
Git
 ↓
pnpm install --frozen-lockfile
 ↓
pnpm run build
 ↓
Vite
 ↓
SSR + prerender
 ↓
dist/public
 ↓
Nginx
```

## 3. Prerendering

Le script `scripts/prerender.mjs` utilise une stratégie hybride :

- SSR React avec `react-dom/server` pour les pages simples ;
- HTML statique pour `/map` et `/dashboard` afin de ne pas exécuter Leaflet dans Node.

Le résultat existe dans `dist/public/fr`, `dist/public/mg` et `dist/public/en`.

## 4. Domaine public principal

```
https://jerymotro.duckdns.org
```

Ce domaine sert le frontend.

## 5. API

```
https://api.jerymotro.duckdns.org
          ↓
http://localhost:8200
```

FastAPI/Uvicorn reste donc derrière Nginx.

## 6. Qdrant

```
https://rag.jerymotro.duckdns.org
          ↓
http://localhost:6333
```

Qdrant est la base vectorielle utilisée par le workflow Chat pour les recherches dans la base de connaissances.

## 7. n8n et Chat

```
https://n8n.jerymotro.duckdns.org
          ↓
http://localhost:5678
```

n8n orchestre le workflow conversationnel.

Pour le Chat :
- question portant sur les données métier → n8n accède à la base relationnelle des feux ;
- question nécessitant des documents/connaissances → n8n utilise Qdrant ;
- besoin combiné → n8n peut réunir les contextes avant la génération.

## 8. WAHA

```
https://waha.jerymotro.duckdns.org
          ↓
http://localhost:3001
```

Utilisé pour WhatsApp.

## 9. Mattermost

```
https://chat.jerymotro.duckdns.org
          ↓
http://localhost:8065
```

Nginx transmet les en-têtes nécessaires aux WebSockets et configure des timeouts adaptés.

## 10. SMSGate

```
https://api.smsgate.jerymotro.duckdns.org
          ↓
localhost:3030

https://smsgate.jerymotro.duckdns.org
          ↓
localhost:3031
```

L'API est utilisée par le backend lorsque le provider SMS sélectionné est SMSGate.

## 11. TLS / Certbot

Nginx termine TLS sur 443 avec des certificats gérés par Certbot.

Flux externe :

```
Client
  ↓ HTTPS / 443
Nginx
  ↓ HTTP localhost
Service
```

## 12. Routage linguistique

La configuration Nginx utilise :

```nginx
map $http_accept_language $prerender_lang {
    default                 fr;
    ~*(^|,\s*)(mg)         mg;
    ~*(^|,\s*)(en)         en;
    ~*(^|,\s*)(fr)         fr;
}
```

Ainsi une requête à `/` peut recevoir :
- `/fr/index.html` ;
- `/mg/index.html` ;
- `/en/index.html`.

## 13. Sitemap et robots

Le build produit `sitemap.xml` à partir des routes pré-rendues.

Dans la version DuckDNS de référence :

```
https://jerymotro.duckdns.org/sitemap.xml
https://jerymotro.duckdns.org/robots.txt
```

Voir [24 — SEO, prerender, sitemap et robots](24_SEO_PRERENDER_SITEMAP_ROBOTS.md).

## 14. Cache

Nginx applique sur les assets :

```nginx
location /assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

Les bundles compilés peuvent donc être mis en cache longuement.

## 15. Validation avant reload

La procédure de production frontend vérifie notamment que le build a produit `dist/` et des fichiers prerenderisés.

Le reload Nginx est précédé de :

```bash
sudo nginx -t
```

puis :

```bash
sudo systemctl reload nginx
```

## 16. Déploiement du backend

Le dépôt backend possède son propre script `deploy.sh`.

Il décrit :

```
git pull --ff-only
 ↓
installation
 ↓
contrôle du port 8200
 ↓
PM2 reload jerymotro-backend --update-env
 ↓
logs PM2
```

Cette procédure est séparée de la publication statique du frontend.

## 17. Stratégie frontend de production

Le script `deploy_prod.sh` est la référence du déploiement statique :

1. vérifier Node/pnpm/Git ;
2. `pnpm install --frozen-lockfile` ;
3. `pnpm run build` ;
4. vérifier le prerender ;
5. nettoyer les anciennes instances frontend PM2 ;
6. tester Nginx ;
7. recharger Nginx ;
8. éventuellement commit/push Git.

Le script précise explicitement que Nginx sert directement `dist/public/`.

## 18. Pourquoi PM2 n'est pas le serveur frontend final ?

Une ancienne stratégie `scripts/deploy.sh` lance `pnpm dev` avec PM2.

La stratégie de production statique décrite ici est différente : le build est figé dans `dist/public` et Nginx sert ces fichiers.

PM2 reste surtout pertinent pour le backend dans la procédure de déploiement correspondante.

## 19. PostgreSQL local sur Debian 13

PostgreSQL est installé et exécuté **localement sur la VM Debian 13**. Il constitue la persistance relationnelle du backend.

```text
FastAPI / SQLAlchemy
        |
      asyncpg
        |
        v
PostgreSQL local
        |
        +--> firms_fire_detections
        +--> fire_events
        +--> alerts / subscriptions
        +--> users / zones
        +--> predictions
```

PostgreSQL n'est pas exposé par Nginx comme les services HTTP. Le trafic SQL reste séparé du routage Web.

La chaîne exacte d'authentification SQL est fournie au runtime par `DATABASE_URL` et n'est pas reproduite ici.

## 20. Ports internes

| Service | Port |
|---|---:|
| PostgreSQL | 5432 |
| FastAPI | 8200 |
| Qdrant | 6333 |
| WAHA | 3001 |
| Mattermost | 8065 |
| n8n | 5678 |
| SMSGate API | 3030 |
| SMSGate Web | 3031 |

Le port PostgreSQL est indiqué comme **port de service interne**, pas comme port publié par Nginx.

## 21. Ports internes

| Service | Port |
|---|---:|
| FastAPI | 8200 |
| Qdrant | 6333 |
| WAHA | 3001 |
| Mattermost | 8065 |
| n8n | 5678 |
| SMSGate API | 3030 |
| SMSGate Web | 3031 |

## 22. Ce qui n'est pas déduit de Nginx

Cette configuration ne révèle pas :
- le mot de passe PostgreSQL ;
- les collections Qdrant ;
- les credentials n8n ;
- le modèle IA sélectionné ;
- les clés d'API.

Ces éléments restent des secrets ou des paramètres runtime.

## 23. Documentation associée

- `23_STRATEGIE_DEPLOIEMENT_DUCKDNS.md` : stratégie détaillée.
- `24_SEO_PRERENDER_SITEMAP_ROBOTS.md` : SEO et fichiers robots/sitemap.
- `18_NGINX_ET_ACCES_RESEAU.md` : routage réseau détaillé.

---

**Navigation :** [[15_PREDICTIONS_J_PLUS_1|← Précédent]] | [[00_INDEX|Index]] | [[17_HUGGING_FACE_DATA_ET_SCRIPTS|Suivant →]]
