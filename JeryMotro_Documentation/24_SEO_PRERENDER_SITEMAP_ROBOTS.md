# SEO technique — SSR, SSG, sitemap.xml et robots.txt

## 1. Objectif

La version DuckDNS du frontend JeryMotro utilise un rendu hybride pour les pages publiques :

- SSR React pour certaines pages ;
- HTML statique pré-rendu pour les pages complexes ;
- SPA React côté navigateur pour l'interactivité.

L'objectif est de fournir du HTML exploitable avant l'exécution complète du JavaScript.

## 2. Chaîne de build

```
pnpm run build
      |
      +--> Vite client
      |
      +--> Vite SSR
      |
      +--> postbuild
               |
               v
       scripts/prerender.mjs
               |
        +------+------+
        |             |
        v             v
     React SSR    HTML statique
        |             |
        +------+------+
               |
               v
          dist/public/
```

Le résultat est ensuite servi par Nginx.

## 3. Routes SSR

Le script `scripts/prerender.mjs` prévoit notamment :

- `/`
- `/login`
- `/register`
- `/legal`
- `/privacy`
- `/about`
- `/cv`

pour les langues `fr`, `mg` et `en`.

## 4. Routes HTML statiques

Les routes `/map` et `/dashboard` sont rendues sous forme de HTML statique léger.

Cette séparation évite d'exécuter Leaflet côté Node, car la carte dépend de l'environnement navigateur.

Au chargement normal, le bundle React prend ensuite le relais.

## 5. Arborescence

Le résultat attendu est :

```
dist/public/
├── index.html
├── assets/
├── robots.txt
├── sitemap.xml
├── fr/
│   ├── index.html
│   ├── login/index.html
│   ├── register/index.html
│   ├── map/index.html
│   └── dashboard/index.html
├── mg/
└── en/
```

## 6. URL canonique DuckDNS

La référence de cette documentation est :

```
https://jerymotro.duckdns.org
```

La variable de build à utiliser pour cette variante est :

```
PRERENDER_BASE_URL=https://jerymotro.duckdns.org
```

Cette valeur est utilisée pour construire les URL absolues des métadonnées SEO et du sitemap.

## 7. Sitemap.xml

Le générateur appelle `generateSitemap()` et écrit :

```
dist/public/sitemap.xml
```

Chaque entrée est construite à partir des routes pré-rendues et des trois langues.

Les éléments générés comprennent :

```xml
<loc>...</loc>
<lastmod>...</lastmod>
<changefreq>...</changefreq>
<priority>...</priority>
<xhtml:link rel="alternate" hreflang="..."/>
```

Le namespace XHTML est utilisé pour les variantes linguistiques.

## 8. Langues dans le sitemap

Le système associe notamment :

```
fr-MG → /fr/
mg    → /mg/
en    → /en/
x-default → /fr/
```

Le même principe est utilisé pour les routes `map`, `dashboard`, `login`, `register`, etc.

## 9. Exposition Nginx du sitemap

La configuration DuckDNS contient :

```nginx
location = /sitemap.xml {
    try_files /sitemap.xml =404;
}
```

Le sitemap est donc un fichier statique servi directement par Nginx.

URL :

```
https://jerymotro.duckdns.org/sitemap.xml
```

## 10. robots.txt

Source frontend :

```
artifacts/jerymotro/public/robots.txt
```

Pour la version DuckDNS de référence :

```text
User-agent: *
Allow: /
Sitemap: https://jerymotro.duckdns.org/sitemap.xml
```

### Signification

`User-agent: *`
→ règle générale pour les robots.

`Allow: /`
→ autorise l'exploration du site.

`Sitemap: ...`
→ indique explicitement au robot où récupérer le sitemap.

## 11. Différence entre robots.txt et sitemap.xml

`robots.txt` ne constitue pas une liste des pages.

Il indique des règles d'exploration et peut déclarer l'emplacement du sitemap.

`sitemap.xml` fournit une liste structurée d'URL que le site souhaite présenter aux moteurs de recherche.

## 12. Détection de langue côté Nginx

La configuration utilise :

```nginx
map $http_accept_language $prerender_lang {
    default                 fr;
    ~*(^|,\s*)(mg)         mg;
    ~*(^|,\s*)(en)         en;
    ~*(^|,\s*)(fr)         fr;
}
```

Exemple :

```
GET /
Accept-Language: mg
        ↓
prerender_lang = mg
        ↓
/mg/index.html
```

Le français est la valeur par défaut.

## 13. Routes principales

La configuration utilise des règles `try_files` spécifiques :

```
/
 /login
 /register
 /map
 /dashboard
```

Pour les variantes localisées :

```
/fr/...
/mg/...
/en/...
```

Le serveur choisit d'abord le fichier statique correspondant.

## 14. Fallback SPA

Pour les autres routes, Nginx utilise :

```nginx
try_files $uri $uri/ /index.html;
```

Cela permet au routeur React/Wouter de gérer les routes côté client lorsque le fichier statique spécifique n'existe pas.

## 15. Balises SEO générées

Le script réalise un audit des éléments suivants :

- `<title>` ;
- `meta description` ;
- `meta robots` ;
- canonical ;
- `og:url` ;
- hreflang ;
- `<h1>`.

Le script contrôle également :
- exactement un `<title>` ;
- exactement un canonical ;
- la présence de l'hôte attendu dans les URL SEO.

## 16. Open Graph

Les pages pré-rendues possèdent des métadonnées permettant aux services sociaux de récupérer notamment :
- titre ;
- description ;
- image ;
- URL.

L'URL doit rester cohérente avec le domaine DuckDNS de référence.

## 17. Cache des assets

Nginx utilise :

```nginx
location /assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

Les fichiers CSS/JS générés peuvent donc bénéficier d'un cache très long.

## 18. Validation après publication

Sur le serveur :

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Tests HTTP :

```bash
curl -I https://jerymotro.duckdns.org/
curl -I https://jerymotro.duckdns.org/robots.txt
curl -I https://jerymotro.duckdns.org/sitemap.xml
curl https://jerymotro.duckdns.org/robots.txt
curl https://jerymotro.duckdns.org/sitemap.xml
curl https://jerymotro.duckdns.org/fr/map/
```

Le dernier test permet notamment de vérifier qu'un HTML pré-rendu existe avant l'exécution complète du SPA.

## 19. Cohérence SEO à respecter

Pour un déploiement DuckDNS cohérent :

```
canonical
   ↓
https://jerymotro.duckdns.org/...

sitemap
   ↓
https://jerymotro.duckdns.org/sitemap.xml

robots.txt
   ↓
Sitemap: https://jerymotro.duckdns.org/sitemap.xml
```

Les trois doivent pointer vers la même origine de référence.

## 20. Écart de traçabilité

Le dépôt frontend contient actuellement un `robots.txt` dont la directive Sitemap pointe vers une autre origine de publication.

Cette documentation **ne prend pas cette autre origine comme référence**, conformément au choix demandé : la stratégie académique de déploiement décrite ici utilise DuckDNS.

Ce constat est conservé pour éviter qu'une incohérence entre artefacts soit transformée en fausse affirmation.

## 21. Résumé

```
React/Vite
   ↓
build
   ↓
SSR + HTML statique
   ↓
dist/public/
   ├── fr/
   ├── mg/
   ├── en/
   ├── sitemap.xml
   └── robots.txt
            ↓
          Nginx
            ↓
https://jerymotro.duckdns.org
```
