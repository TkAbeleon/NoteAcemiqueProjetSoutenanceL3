# Stratégie de déploiement — version DuckDNS

> **Périmètre de cette documentation :** cette page décrit la variante de déploiement **DuckDNS + Nginx** utilisée comme référence pour la présentation technique de JeryMotro.
>
> Une autre chaîne CI existe actuellement dans le dépôt frontend avec une cible différente. Elle n'est pas utilisée comme architecture de référence dans cette documentation afin de conserver le déploiement DuckDNS demandé.

## 1. Objectif du déploiement

Le frontend JeryMotro est construit comme un site Web statique après compilation.

Le serveur de production n'a donc pas besoin de faire tourner React ou Vite pour servir les pages finales.

Le principe est :

```
Code Git
   ↓
pnpm install
   ↓
pnpm run build
   ↓
Vite build
   ↓
SSR + prerender
   ↓
dist/public/
   ↓
Nginx
   ↓
https://jerymotro.duckdns.org
```

## 2. Build frontend

Le package `@workspace/jerymotro` déclare :

```text
pnpm run build
  ├─ vite build
  ├─ vite build --ssr src/entry-server.tsx
  └─ postbuild → scripts/prerender.mjs
```

Le build produit :
- bundle JavaScript ;
- CSS ;
- assets ;
- bundle SSR temporaire ;
- pages HTML prerenderisées ;
- sitemap.xml.

## 3. Prerendering hybride

`scripts/prerender.mjs` utilise deux stratégies.

### SSR React

Les routes publiques suivantes sont rendues avec React côté Node :

- `/`
- `/login`
- `/register`
- `/legal`
- `/privacy`
- `/about`
- `/cv`

### HTML statique pour les pages complexes

Les routes :
- `/map`
- `/dashboard`

sont générées en HTML statique léger afin de ne pas exécuter Leaflet dans Node.

Le navigateur charge ensuite le bundle React et l'application interactive.

## 4. Langues

Le prerender est généré pour :
- `fr`
- `mg`
- `en`

La structure est :

```
dist/public/
├── fr/
│   ├── index.html
│   ├── login/index.html
│   ├── register/index.html
│   ├── map/index.html
│   └── ...
├── mg/
│   └── ...
├── en/
│   └── ...
├── assets/
├── sitemap.xml
└── ...
```

## 5. BASE_URL DuckDNS

Pour cette architecture, l'URL canonique de génération doit être :

```
PRERENDER_BASE_URL=https://jerymotro.duckdns.org
```

Le générateur utilise cette valeur pour :
- `canonical` ;
- `og:url` ;
- `hreflang` ;
- `sitemap.xml`.

La propriété est importante : si une autre URL est fournie pendant le build, les liens SEO peuvent référencer cette autre origine.

## 6. Sitemap.xml

Le sitemap est généré automatiquement par `scripts/prerender.mjs`.

Il utilise le namespace Sitemap 0.9 et le namespace XHTML pour les alternatives linguistiques.

Pour chaque route pré-rendue et chaque langue, le générateur construit :
- `<loc>` ;
- `<lastmod>` ;
- `<changefreq>` ;
- `<priority>` ;
- `hreflang` fr-MG ;
- `hreflang` mg ;
- `hreflang` en ;
- `hreflang=x-default`.

Le fichier final est :

```
dist/public/sitemap.xml
```

Nginx le sert directement :

```
location = /sitemap.xml {
    try_files /sitemap.xml =404;
}
```

Dans la variante DuckDNS documentée, l'URL logique du sitemap est :

```
https://jerymotro.duckdns.org/sitemap.xml
```

## 7. robots.txt

Le fichier `robots.txt` est un fichier statique public destiné aux robots d'indexation.

Pour la variante DuckDNS de cette documentation, le contenu attendu est :

```
User-agent: *
Allow: /
Sitemap: https://jerymotro.duckdns.org/sitemap.xml
```

Le point important est que la directive `Sitemap` doit pointer vers **la même origine canonique que le sitemap et les balises SEO**.

> La copie `robots.txt` actuellement visible dans le dépôt frontend contient une autre origine. Cette différence appartient à une autre cible de publication et n'est pas utilisée comme référence dans cette documentation DuckDNS.

## 8. Audit SEO pendant le build

`prerender.mjs` réalise un audit automatique pour les pages pré-rendues.

Le script vérifie notamment :
- `<title>` ;
- `meta description` ;
- `meta robots` ;
- canonical ;
- `og:url` ;
- `hreflang` ;
- `<h1>`.

Il vérifie également qu'il existe exactement :
- un canonical ;
- un title.

Il contrôle enfin que l'hôte de la canonical correspond à `BASE_URL`.

## 9. Déploiement statique Nginx

Le script `deploy_prod.sh` du frontend documente une stratégie de production statique.

### Étape 1 — prérequis

Le script vérifie :
- pnpm ;
- Node.js ;
- Git ;
- présence du frontend ;
- présence de package.json.

Nginx n'est pas bloquant au contrôle initial, mais son absence désactive le reload automatique.

### Étape 2 — dépendances

Le script utilise :

```
pnpm install --frozen-lockfile
```

Il respecte le workspace pnpm du monorepo.

### Étape 3 — build

Le script exécute :

```
pnpm run build
```

Le `postbuild` lance automatiquement le prerender.

### Étape 4 — validation

Le script vérifie l'existence de `dist/` et recherche les HTML pré-rendus dans les dossiers `fr`, `mg` et `en`.

### Étape 5 — PM2

Le script de production arrête les anciennes instances frontend `jerymotro-vite` et `jerymotro-render`.

La logique finale est donc :

> **Nginx sert les fichiers statiques. Aucun processus Node frontend permanent n'est nécessaire pour servir le build.**

### Étape 6 — Nginx

Le script exécute :

```
sudo nginx -t
sudo systemctl reload nginx
```

La nouvelle version du frontend est alors prise en compte sans arrêter Nginx.

### Étape 7 — Git

Le script peut :
- détecter les modifications ;
- créer un commit ;
- pousser vers la branche Git courante.

## 10. Nginx et DuckDNS

La configuration `UML_JeryMotro/conf.ngnix` définit :

```
jerymotro.duckdns.org
        ↓
/mnt/jerymotro/JeryMotro_WEB/artifacts/jerymotro/dist/public
```

Le frontend est donc servi par le système de fichiers.

Pour les routes principales, Nginx utilise `try_files` afin de sélectionner la version prerenderisée correspondant à la langue.

## 11. Détection de langue

La directive Nginx :

```
map $http_accept_language $prerender_lang
```

sélectionne :
- `mg` pour les requêtes demandant Malagasy ;
- `en` pour English ;
- `fr` par défaut.

Exemple :

```
Accept-Language: mg
        ↓
prerender_lang = mg
        ↓
/mg/index.html
```

Le même principe est utilisé pour `/login`, `/register`, `/map` et `/dashboard`.

## 12. SPA fallback

Pour les autres routes :

```
try_files $uri $uri/ /index.html;
```

Cela permet au client React/Wouter de prendre le relais lorsque la ressource statique précise n'existe pas.

## 13. Cache des assets

Nginx applique :

```
location /assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

Les bundles compilés peuvent donc être fortement mis en cache.

## 14. HTTPS

La version DuckDNS utilise :
- port 443 ;
- certificats Let's Encrypt/Certbot ;
- redirection/gestion du port 80 par les blocs Certbot.

Flux :

```
Navigateur
   ↓ HTTPS :443
Nginx
   ↓
fichiers statiques
```

## 15. Séparation frontend/backend

Le frontend est servi par :

`https://jerymotro.duckdns.org`

L'API est séparée sur :

`https://api.jerymotro.duckdns.org`

et Nginx la transmet à :

`http://localhost:8200`.

Cette séparation permet de conserver :
- un domaine Web pour l'interface ;
- un domaine API pour FastAPI ;
- des ports internes non exposés directement.

## 16. Résumé de la stratégie

```
                    Git
                     |
                     v
              pnpm install
                     |
                     v
               Vite build
                     |
             +-------+-------+
             |               |
          SSR React      HTML statique
             |            Leaflet-safe
             +-------+-------+
                     |
                     v
                dist/public
                /    |    \
              fr     mg     en
               \     |     /
                 sitemap.xml
                 robots.txt
                     |
                     v
              Nginx / Certbot
                     |
                     v
        https://jerymotro.duckdns.org
```

## 17. Ce qu'il faut dire à la soutenance

> Le frontend JeryMotro est compilé en amont. Le build Vite est suivi d'un prerendering hybride qui génère des pages HTML pour le référencement. Le répertoire `dist/public` est ensuite servi statiquement par Nginx sur le domaine DuckDNS sécurisé par HTTPS. Le sitemap et les fichiers SEO sont générés ou servis dans cette même arborescence, tandis que l'API FastAPI reste séparée sur son sous-domaine.

## 18. Point de vigilance

Il faut toujours construire le frontend avec la bonne `PRERENDER_BASE_URL`.

Pour la version DuckDNS documentée :

```bash
PRERENDER_BASE_URL=https://jerymotro.duckdns.org pnpm run build
```

Cela évite de générer des canonical, sitemap et métadonnées Open Graph pointant vers une autre plateforme.

---

**Navigation :** [[22_PROTOCOLLES_ET_INTERFACES|← Précédent]] | [[00_INDEX|Index]] | [[24_SEO_PRERENDER_SITEMAP_ROBOTS|Suivant →]]
