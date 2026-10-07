# 📚 Bibliographie et webographie — JeryMotro

#JeryMotro #Bibliographie #Webographie #APA #References #MemoireL3

[[24_SEO_PRERENDER_SITEMAP_ROBOTS|← Précédent]] | [[00_INDEX|Index]] | [[Glossaire_Tags|Glossaire →]]

> Références utilisées pour documenter les technologies, protocoles, sources de données et méthodes réellement présents dans l'architecture JeryMotro.
>
> Les références sont organisées en **bibliographie scientifique/technique** et **webographie officielle**. Les URL ci-dessous correspondent aux ressources officielles ou aux publications originales lorsque celles-ci sont disponibles.

---

## 1. Données satellitaires et environnement

### NASA FIRMS

NASA. (n.d.). *Fire Information for Resource Management System (FIRMS)*. NASA Earthdata. https://firms.modaps.eosdis.nasa.gov/

**Utilisation dans JeryMotro :** source des observations satellitaires de points thermiques utilisées par le pipeline FIRMS.

### Google Earth Engine

Google. (n.d.). *Google Earth Engine documentation*. Google for Developers. https://developers.google.com/earth-engine

**Utilisation dans JeryMotro :** scripts d'enrichissement environnemental et extraction de variables géospatiales.

### ERA5-Land

Muñoz Sabater, J. (2019). *ERA5-Land hourly data from 1981 to present*. Copernicus Climate Change Service (C3S) Climate Data Store. https://doi.org/10.24381/cds.e2161bac

**Utilisation dans JeryMotro :** variables météorologiques utilisées par les scripts d'enrichissement.

### MODIS / NDVI

Didan, K. (2021). *MODIS/Terra vegetation indices monthly L3 global 0.05Deg CMG (MOD13C2)*. NASA EOSDIS Land Processes Distributed Active Archive Center. https://doi.org/10.5067/MODIS/MOD13C2.061

**Utilisation dans JeryMotro :** indice de végétation utilisé dans l'enrichissement environnemental.

### ESA WorldCover

Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., Lesiv, M., Herold, M., Tsendbazar, N. E., Xu, P., Ramoino, F., & Arino, O. (2022). *ESA WorldCover 10 m 2021 v200*. Zenodo. https://doi.org/10.5281/zenodo.7254221

**Utilisation dans JeryMotro :** occupation du sol utilisée par les scripts GEE.

### Hansen Global Forest Change

Hansen, M. C., Potapov, P. V., Moore, R., Hancher, M., Turubanova, S. A., Tyukavina, A., Thau, D., Stehman, S. V., Goetz, S. J., Loveland, T. R., Kommareddy, A., Egorov, A., Chini, L., Justice, C. O., & Townshend, J. R. G. (2013). High-resolution global maps of 21st-century forest cover change. *Science, 342*(6160), 850–853. https://doi.org/10.1126/science.1244693

**Utilisation dans JeryMotro :** information de perte forestière dans l'enrichissement environnemental.

---

## 2. Machine Learning et clustering

### XGBoost

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). ACM. https://doi.org/10.1145/2939672.2939785

**Utilisation dans JeryMotro :** référence méthodologique pour les modèles de gradient boosting ; le service ML externe expose le scoring au backend.

### HDBSCAN

McInnes, L., Healy, J., & Astels, S. (2017). hdbscan: Hierarchical density based clustering. *Journal of Open Source Software, 2*(11), 205. https://doi.org/10.21105/joss.00205

**Utilisation dans JeryMotro :** regroupement spatial des détections FIRMS avant constitution des événements de feu.

### Scikit-learn

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html

**Utilisation dans JeryMotro :** référence de l'écosystème ML Python et du clustering disponible côté backend.

---

## 3. Recherche vectorielle et RAG

### Qdrant

Qdrant. (n.d.). *Qdrant documentation*. https://qdrant.tech/documentation/

**Utilisation dans JeryMotro :** stockage et recherche vectorielle de la base de connaissances utilisée par le workflow n8n.

### Retrieval-Augmented Generation

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems, 33*. https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

**Utilisation dans JeryMotro :** cadre conceptuel pour la séparation entre données structurées SQL et récupération documentaire/vectorielle Qdrant dans le Chat.

---

## 4. Backend, API et base de données

### Python

Python Software Foundation. (n.d.). *Python 3 documentation*. https://docs.python.org/3/

### FastAPI

Ramírez, S. (n.d.). *FastAPI documentation*. https://fastapi.tiangolo.com/

### PostgreSQL

PostgreSQL Global Development Group. (n.d.). *PostgreSQL documentation*. https://www.postgresql.org/docs/

**Utilisation dans JeryMotro :** SGBD relationnel installé localement sur la VM Debian 13.

### SQL

IBM. (n.d.). *Structured Query Language (SQL)*. IBM Think. https://www.ibm.com/think/topics/structured-query-language

### SQLAlchemy

SQLAlchemy. (n.d.). *SQLAlchemy documentation*. https://docs.sqlalchemy.org/

### Alembic

SQLAlchemy. (n.d.). *Alembic documentation*. https://alembic.sqlalchemy.org/

---

## 5. Frontend

### React

Meta Open Source. (n.d.). *React documentation*. https://react.dev/

### Vite

Vite. (n.d.). *Vite documentation*. https://vite.dev/guide/

### TypeScript

Microsoft. (n.d.). *TypeScript documentation*. https://www.typescriptlang.org/docs/

### Leaflet

Leaflet. (n.d.). *Leaflet documentation*. https://leafletjs.com/reference.html

---

## 6. Infrastructure et déploiement

### Debian

Debian Project. (n.d.). *Debian — The universal operating system*. https://www.debian.org/

### Google Cloud Compute Engine

Google Cloud. (n.d.). *Compute Engine documentation*. https://cloud.google.com/compute/docs

**Utilisation dans JeryMotro :** VM hébergeant l'infrastructure de production documentée.

### Nginx

F5, Inc. (n.d.). *NGINX documentation*. https://nginx.org/en/docs/

**Utilisation dans JeryMotro :** reverse proxy, terminaison TLS et routage des sous-domaines DuckDNS.

### Certbot

Electronic Frontier Foundation. (n.d.). *Certbot documentation*. https://eff-certbot.readthedocs.io/

### PM2

PM2. (n.d.). *PM2 documentation*. https://pm2.keymetrics.io/docs/usage/quick-start/

**Utilisation dans JeryMotro :** gestion du processus backend dans la stratégie de déploiement observée.

### Docker

Docker. (n.d.). *Docker documentation*. https://docs.docker.com/

---

## 7. Automatisation et communication

### n8n

n8n GmbH. (n.d.). *n8n documentation*. https://docs.n8n.io/

**Utilisation dans JeryMotro :** orchestration du Chat, accès aux données métier et à Qdrant, ainsi que certaines automatisations.

### WAHA

DevLikePro. (n.d.). *WAHA documentation*. https://waha.devlike.pro/docs/

**Utilisation dans JeryMotro :** passerelle HTTP pour les opérations WhatsApp.

### WhatsApp Business Platform

Meta Platforms, Inc. (n.d.). *WhatsApp Business Platform — Developer Hub*. https://business.whatsapp.com/developers/developer-hub

### SMSGate

SMS Gate. (n.d.). *SMS Gate documentation*. https://docs.sms-gate.app/

### Orange Developer

Orange. (n.d.). *Orange Developer — SMS API Madagascar*. https://developer.orange.com/apis/sms-mg

---

## 8. Versioning, code et hébergement de données

### Git

Git Project. (n.d.). *Git documentation*. https://git-scm.com/docs

### GitHub

GitHub. (n.d.). *GitHub Docs*. https://docs.github.com/

### Hugging Face

Hugging Face. (n.d.). *Hugging Face documentation*. https://huggingface.co/docs

**Utilisation dans JeryMotro :** hébergement/partage des datasets et de certaines briques complémentaires du projet.

### Dataset JeryMotro

rtsikynyantsa. (n.d.). *MADAGASCAR_GEE_FIMRS* [Dataset]. Hugging Face. https://huggingface.co/datasets/rtsikynyantsa/MADAGASCAR_GEE_FIMRS

**Utilisation dans JeryMotro :** dataset Madagascar lié aux traitements FIRMS/GEE.

---

## 9. DNS et protocoles Web

### DuckDNS

DuckDNS. (n.d.). *Duck DNS*. https://www.duckdns.org/

**Utilisation dans JeryMotro :** domaine dynamique de la configuration de référence :

```text
jerymotro.duckdns.org
```

### DNS

Mockapetris, P. (1987). *Domain names — Concepts and facilities* (RFC 1034). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc1034

### HTTPS / TLS

Internet Engineering Task Force. (2018). *The transport layer security (TLS) protocol version 1.3* (RFC 8446). https://www.rfc-editor.org/rfc/rfc8446

---

## 10. Modélisation

### PlantUML

PlantUML. (n.d.). *PlantUML documentation*. https://plantuml.com/

**Utilisation dans JeryMotro :** diagrammes d'architecture et de déploiement associés à la documentation.

---

## 11. Références directement liées à l'infrastructure JeryMotro

| Élément | Référence | Rôle dans le projet |
|---|---|---|
| FIRMS | NASA FIRMS | Source des feux |
| GEE | Google Earth Engine | Enrichissement |
| PostgreSQL | PostgreSQL Documentation | BDD relationnelle locale |
| Qdrant | Qdrant Documentation | Recherche vectorielle |
| n8n | n8n Documentation | Orchestration |
| Nginx | NGINX Documentation | Reverse proxy |
| Debian 13 | Debian Project | OS de la VM |
| GCP | Google Cloud | Infrastructure VM |
| DuckDNS | DuckDNS | Domaine de référence |
| Hugging Face | Hugging Face | Datasets |
| React | React Documentation | Frontend |
| FastAPI | FastAPI Documentation | Backend |
| HDBSCAN | McInnes et al. (2017) | Clustering |
| XGBoost | Chen & Guestrin (2016) | Référence ML |
| RAG | Lewis et al. (2020) | Fondement du Chat documentaire |

---

## 12. Règle bibliographique pour le mémoire

Pour le mémoire, il est préférable de citer :

- **les publications scientifiques originales** pour les méthodes ML et les jeux de données scientifiques ;
- **les documentations officielles** pour les frameworks, logiciels et services ;
- **la page officielle du dataset** pour les données Hugging Face ;
- **la configuration du dépôt JeryMotro** comme source primaire de l'implémentation.

Une documentation technique ne doit pas être utilisée comme preuve qu'une fonction existe dans JeryMotro : cette preuve vient du code, de la configuration ou d'un test reproductible.

---

**Navigation :** [[24_SEO_PRERENDER_SITEMAP_ROBOTS|← Précédent]] | [[00_INDEX|Index]] | [[Glossaire_Tags|Glossaire →]]
