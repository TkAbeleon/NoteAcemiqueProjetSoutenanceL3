# 📋 Cahier des Charges Fonctionnel et Technique — JeryMotro

#JeryMotro #MemoireL3 #CahierDesCharges #Specification #Technique
[[Glossaire_Tags]] | [[00_INDEX]]

> **Document de référence fonctionnel et technique pour la documentation du système JeryMotro.**
> Version 1.0 — 07/10/2026.
>
> **Méthode :** les exigences sont confrontées à l'état observé dans les dépôts JeryMotro_WEB et JeryMotroBackend, à la configuration Nginx de référence et aux scripts/datasets associés. Une exigence n'est pas considérée comme une fonction opérationnelle uniquement parce qu'elle apparaît dans une ancienne note de conception.

---

## 1. IDENTIFICATION DU PROJET

| Champ | Valeur |
|---|---|
| **Nom** | JeryMotro |
| **Nature** | Plateforme logicielle académique de surveillance et d'analyse des feux de végétation |
| **Territoire principal** | Madagascar |
| **Frontend** | Application Web React/Vite |
| **Backend** | API FastAPI / Python |
| **Persistance métier** | Base SQL accessible par le backend |
| **Source principale des détections** | NASA FIRMS |
| **Analyse ML** | Service ML externe, contrat HTTP depuis le backend |
| **Clustering** | HDBSCAN avec fallback grille |
| **Enrichissement environnemental** | Scripts Google Earth Engine séparés |
| **Chat IA** | FastAPI → webhook n8n → accès SQL et/ou Qdrant → modèle IA |
| **Reverse proxy de référence** | Nginx |
| **Domaine Web de référence** | https://jerymotro.duckdns.org |
| **Infrastructure documentée** | GCP / Debian 13 / Nginx / services locaux |
| **Référentiel du code** | GitHub |
| **Données/scripts complémentaires** | Hugging Face |

---

## 2. CONTEXTE ET PROBLÉMATIQUE

Les données NASA FIRMS fournissent des détections satellitaires de points thermiques. Ces observations sont utiles mais ne constituent pas, à elles seules, une application de suivi opérationnel.

JeryMotro ajoute une couche logicielle destinée à :

1. collecter les détections ;
2. les normaliser et éviter les doublons ;
3. vérifier leur cohérence géographique ;
4. rattacher les observations aux régions ;
5. calculer ou récupérer un niveau de risque ;
6. regrouper spatialement les observations ;
7. représenter ces groupes comme des événements de feu ;
8. suivre leur évolution temporelle ;
9. exposer les résultats par API et interface Web ;
10. déclencher des alertes selon des seuils ;
11. permettre des interrogations conversationnelles via n8n ;
12. exploiter une base de connaissances vectorielle via Qdrant lorsque nécessaire.

---

## 3. OBJECTIF GÉNÉRAL

Construire une plateforme Web capable de transformer des observations satellitaires de feux en informations exploitables : données nettoyées, contexte géographique, score de risque, événements regroupés, état temporel, visualisation, analyse et notification.

---

## 4. OBJECTIFS SPÉCIFIQUES

| ID | Objectif | État observé |
|---|---|---|
| OS-01 | Collecter automatiquement les données FIRMS | **Réel** |
| OS-02 | Normaliser les données et calculer des variables dérivées | **Réel** |
| OS-03 | Dédupliquer les observations | **Réel** |
| OS-04 | Vérifier la cohérence géographique Madagascar | **Réel** |
| OS-05 | Identifier une région administrative | **Réel** |
| OS-06 | Obtenir un score de risque ML | **Intégration externe + fallback local** |
| OS-07 | Regrouper les observations proches | **Réel** |
| OS-08 | Maintenir un événement de feu | **Réel, avec limites documentées** |
| OS-09 | Diffuser des alertes | **Réel, dépendant des services externes** |
| OS-10 | Servir une interface cartographique et analytique | **Réel** |
| OS-11 | Fournir un Chat IA | **Réel au niveau de l'intégration FastAPI/n8n** |
| OS-12 | Utiliser SQL pour les questions sur les données de feux | **Architecture confirmée** |
| OS-13 | Utiliser Qdrant pour la base de connaissances | **Architecture confirmée** |
| OS-14 | Enrichir les données via GEE | **Réel sous forme de scripts séparés** |
| OS-15 | Générer automatiquement toute une chaîne J+1 | **Non démontré dans le pipeline principal** |

---

## 5. PÉRIMÈTRE FONCTIONNEL

### 5.1 Inclus

- collecte NASA FIRMS ;
- traitement des observations de type point ;
- géofiltrage ;
- attribution de région ;
- scoring de risque ;
- clustering ;
- suivi des événements ;
- statistiques ;
- carte Web ;
- comptes utilisateurs ;
- rôles Standard / Premium / Admin ;
- abonnements aux alertes ;
- OTP de vérification des destinations ;
- Email / WhatsApp / SMS selon configuration ;
- Chat IA ;
- accès SQL aux données de feu depuis le workflow n8n ;
- accès Qdrant à la base de connaissances depuis le workflow n8n ;
- enrichissement environnemental GEE séparé ;
- déploiement DuckDNS + Nginx de référence ;
- SEO, prerender, sitemap et robots.txt.

### 5.2 Hors périmètre du fonctionnement principal démontré

- preuve terrain automatique ;
- garantie qu'un feu est réellement éteint ;
- détection autonome complète de la déforestation ;
- preuve qu'une accuracy affichée dans l'interface est une mesure scientifique ;
- génération automatiquement démontrée de chaque prédiction J+1 ;
- exécution directe de Qdrant ou du moteur IA dans rag_service.py.

---

## 6. ACTEURS

| Acteur | Responsabilité |
|---|---|
| **Utilisateur public** | Consulte les pages publiques et les informations disponibles |
| **Utilisateur Standard** | Consulte les données et fonctions autorisées |
| **Utilisateur Premium** | Accède aux fonctions Premium, zones et canaux d'alertes autorisés |
| **Administrateur** | Gère utilisateurs, demandes d'accès et opérations internes |
| **NASA FIRMS** | Fournit les observations satellitaires |
| **Service ML** | Retourne le score de risque et le label |
| **Google Earth Engine** | Fournit des variables environnementales aux scripts d'enrichissement |
| **n8n** | Orchestre le Chat et les automatisations |
| **Qdrant** | Fournit la recherche vectorielle de la base de connaissances |
| **Services de notification** | Envoient les messages externes |

---

## 7. EXIGENCES FONCTIONNELLES

### 7.1 Ingestion FIRMS

**EF-01 — Collecte**

Le système doit pouvoir interroger l'API NASA FIRMS pour récupérer des détections correspondant aux sources et à la zone configurées.

**EF-02 — Reprise de collecte**

Le système doit pouvoir reprendre une collecte à partir de la dernière date connue avec une fenêtre permettant de limiter les trous de données.

**EF-03 — Normalisation**

Chaque ligne exploitable doit être transformée vers le modèle interne FirmsFireDetection.

**EF-04 — Déduplication**

L'insertion doit empêcher les doublons logiques selon les clés définies dans le modèle SQL.

### 7.2 Validation géographique

**EF-05 — Contrôle de coordonnées**

Les coordonnées doivent être valides avant insertion.

**EF-06 — Filtrage Madagascar**

Le backend utilise une bbox de sécurité et un contrôle géographique.

**EF-07 — Attribution régionale**

Le backend doit rechercher la région via les géométries GeoJSON et Shapely.

**EF-08 — Fallback géocodage**

Un service de reverse geocoding peut être utilisé en repli selon configuration.

### 7.3 Évaluation du risque

**EF-09 — Scoring externe**

Le backend doit pouvoir appeler le service ML via :

~~~text
POST <ML_SERVICE_URL>/predict
~~~

**EF-10 — Résultat**

Le service ML retourne au minimum un risk_score et un fire_label selon le contrat client.

**EF-11 — Fallback**

En cas d'indisponibilité du ML ou de score inutilisable, le backend doit pouvoir produire un score heuristique de repli.

**EF-12 — Niveau de risque**

Le backend transforme le score et certaines règles FRP en niveaux métier.

### 7.4 Clustering et événements

**EF-13 — Clustering**

Le système doit regrouper les détections proches avec HDBSCAN lorsqu'il est disponible.

**EF-14 — Fallback clustering**

Une grille géographique doit pouvoir être utilisée si HDBSCAN n'est pas disponible.

**EF-15 — FireEvent**

Le groupe résultant doit pouvoir être stocké comme événement de feu avec centre, taille, FRP, risque, région et dates.

**EF-16 — Suivi temporel**

Le système doit calculer un statut temporel à partir de la dernière observation.

### 7.5 Alertes

**EF-17 — Abonnement**

Un utilisateur autorisé doit pouvoir enregistrer une destination et des seuils min_risk / min_frp.

**EF-18 — Vérification**

Une destination à vérifier doit utiliser un OTP avec expiration et contrôle des tentatives.

**EF-19 — Déclenchement**

Une alerte peut être candidate si :

~~~text
risk_score >= min_risk OR frp >= min_frp
~~~

ou selon une action administrative forcée.

**EF-20 — Canaux**

Les canaux configurés sont :
- Email via n8n ;
- WhatsApp via WAHA ;
- SMS via provider configuré.

### 7.6 Chat IA et RAG

**EF-21 — Interface**

Le frontend doit transmettre la question au backend.

**EF-22 — Orchestration n8n**

FastAPI doit relayer la question à n8n par webhook HTTP(S).

**EF-23 — Données métier**

Pour une question portant sur les données JeryMotro, le workflow n8n doit pouvoir interroger la base relationnelle des feux.

**EF-24 — Base de connaissances**

Lorsque la question nécessite des documents ou connaissances textuelles, n8n doit pouvoir interroger Qdrant.

**EF-25 — Contexte combiné**

Le workflow peut combiner les résultats SQL et vectoriels avant la génération de la réponse.

**EF-26 — Réponse**

FastAPI doit normaliser la réponse du workflow avant de la transmettre au frontend.

### 7.7 Interface Web

**EF-27 — Carte**

L'application doit permettre de visualiser les détections et événements.

**EF-28 — Filtrage**

Les pages métier doivent permettre le filtrage par les critères réellement exposés par l'API.

**EF-29 — Analyse**

Le frontend doit afficher les statistiques et informations environnementales disponibles.

**EF-30 — Export**

L'interface doit permettre la préparation des exports supportés.

---

## 8. DONNÉES ET PERSISTANCE

### 8.1 Données FIRMS

Le modèle principal contient notamment :

latitude, longitude, acq_date, acq_time, satellite, instrument, brightness, bright_t31, frp, confidence, daynight, scan, track.

### 8.2 Variables dérivées

Le backend peut calculer notamment :

- diff_brightness ;
- frp_log ;
- confidence_num ;
- scan_track_ratio ;
- local_hour ;
- is_dry_season.

### 8.3 Variables environnementales

Selon les données disponibles :

- température ;
- humidité relative ;
- vent ;
- précipitation ;
- landcover ;
- pente ;
- NDVI ;
- perte forestière récente.

### 8.4 Événements

Un FireEvent regroupe notamment :

- centre ;
- taille ;
- FRP total ;
- FRP maximum ;
- risque maximum ;
- niveau ;
- région ;
- première observation ;
- dernière observation ;
- durée ;
- statut.

---

## 9. ARCHITECTURE TECHNIQUE DE RÉFÉRENCE

~~~text
Utilisateur
    |
    | HTTPS
    v
Nginx
    |
    +------------------> Frontend statique
    |
    +------------------> FastAPI :8200
                              |
                +-------------+------------------+
                |             |                  |
                v             v                  v
             Base SQL      NASA FIRMS         ML Service
                |
                +<-------- n8n <-------- Webhook / Chat
                             |
                             +--------> Base SQL des feux
                             |
                             +--------> Qdrant :6333
                             |
                             +--------> Modèle IA
~~~

### Architecture de déploiement

~~~text
GCP / Debian 13
       |
     Nginx
       |
       +-- jerymotro.duckdns.org
       +-- api.jerymotro.duckdns.org
       +-- rag.jerymotro.duckdns.org
       +-- n8n.jerymotro.duckdns.org
       +-- waha.jerymotro.duckdns.org
       +-- chat.jerymotro.duckdns.org
       +-- api.smsgate.jerymotro.duckdns.org
       +-- smsgate.jerymotro.duckdns.org
~~~

La configuration de référence est UML_JeryMotro/conf.ngnix.

---

## 10. AUTOMATISATION DU PIPELINE

Le backend possède une boucle de collecte interne à FastAPI.

~~~text
Démarrage backend
       |
       v
run_automatic_pipeline()
       |
       +--> collecte FIRMS
       +--> région
       +--> scoring
       +--> clustering
       +--> alertes candidates
       |
       v
attente intervalle
       |
       v
nouveau cycle
~~~

L'intervalle par défaut observé dans le code actuel est de **3 heures**, et ne doit pas être confondu avec l'ancien cahier des charges qui mentionnait 30 minutes via n8n.

---

## 11. ENRICHISSEMENT GEE

Les scripts GEE sont une chaîne séparée :

~~~text
FIRMS / dataset
      |
      v
Google Earth Engine
      |
      +--> ERA5-Land
      +--> NASADEM
      +--> ESA WorldCover
      +--> Hansen Global Forest Change
      +--> MODIS NDVI
      |
      v
Dataset enrichi
~~~

Cette chaîne n'est pas appelée directement par run_automatic_pipeline().

---

## 12. CHAT : DÉCISION DE ROUTAGE DES CONNAISSANCES

Le Chat doit distinguer deux classes de sources.

| Besoin | Source |
|---|---|
| Données structurées de détections | Base SQL des feux |
| Événements / indicateurs | Base SQL des feux |
| Documents / connaissances textuelles | Qdrant |
| Question mixte | SQL + Qdrant |
| Génération | Modèle IA du workflow n8n |

Cette séparation est une contrainte d'architecture.

---

## 13. API ET CONTRATS

### Frontend → FastAPI

Protocole : HTTPS / JSON.

Le frontend utilise des routes métier pour :
- authentification ;
- détections ;
- événements ;
- statistiques ;
- alertes ;
- Chat ;
- zones ;
- prédictions.

### FastAPI → ML

Protocole : HTTP(S) / JSON.

Contrat principal :

~~~text
POST <ML_SERVICE_URL>/predict
~~~

### FastAPI → n8n

Protocole : HTTP(S) / JSON.

Le backend appelle le webhook n8n avec :
- message ;
- contexte conversationnel ;
- utilisateur ;
- rôle ;
- zone éventuelle.

### n8n → SQL

Accès aux données relationnelles des feux pour les questions métier.

### n8n → Qdrant

Accès vectoriel à la base de connaissances pour la recherche sémantique.

---

## 14. EXIGENCES NON FONCTIONNELLES

| Catégorie | Exigence |
|---|---|
| **Sécurité** | Les secrets ne doivent jamais être écrits dans la documentation ni dans Git |
| **Transport** | Les accès publics doivent passer par HTTPS |
| **API** | Les contrats JSON doivent être stables et validés |
| **Performance** | Les traitements lourds doivent éviter de bloquer le serveur HTTP |
| **Disponibilité** | Les dépendances externes doivent avoir des comportements d'échec contrôlés |
| **Données** | Les NULL doivent rester distincts de zéro dans les analyses |
| **Observabilité** | Les erreurs des services externes doivent être journalisées |
| **Déploiement** | Le frontend produit doit pouvoir être servi statiquement par Nginx |
| **SEO** | Le domaine canonique, sitemap et robots doivent rester cohérents |
| **Maintenabilité** | Les services métier doivent rester séparés par responsabilité |

---

## 15. SÉCURITÉ

### Authentification

Le backend utilise des jetons JWT.

### Autorisation

Les dépendances backend distinguent notamment :
- utilisateur connecté ;
- Premium ;
- Admin.

### Secrets

Les documentations doivent utiliser uniquement les noms de variables :
- DATABASE_URL ;
- JWT_SECRET ;
- FIRMS_MAP_KEY ;
- ML_SERVICE_API_KEY ;
- credentials GEE ;
- webhook n8n ;
- credentials WAHA ;
- credentials SMS ;
- secrets Hugging Face / Doppler.

### Règle

> Aucune valeur réelle de clé, token, mot de passe ou credential ne doit apparaître dans ce cahier des charges.

---

## 16. DÉPLOIEMENT

### Frontend

~~~text
Git
 ↓
pnpm install --frozen-lockfile
 ↓
pnpm run build
 ↓
Vite client + Vite SSR
 ↓
prerender
 ↓
dist/public
 ↓
Nginx
~~~

### Backend

~~~text
Git
 ↓
installation dépendances
 ↓
processus backend
 ↓
Uvicorn / FastAPI
 ↓
localhost:8200
 ↓
Nginx
~~~

### Services auxiliaires de référence

| Service | Port interne |
|---|---:|
| FastAPI | 8200 |
| Qdrant | 6333 |
| WAHA | 3001 |
| Mattermost | 8065 |
| n8n | 5678 |
| SMSGate API | 3030 |
| SMSGate Web | 3031 |

---

## 17. SEO ET INDEXATION

Le frontend public doit fournir :
- HTML prerenderisé ;
- sitemap.xml ;
- robots.txt ;
- canonical ;
- hreflang ;
- Open Graph.

Origine de référence :

https://jerymotro.duckdns.org

Sitemap :

https://jerymotro.duckdns.org/sitemap.xml

Robots :

https://jerymotro.duckdns.org/robots.txt

Les trois doivent rester cohérents avec la même origine canonique.

---

## 18. CRITÈRES D'ACCEPTATION

| ID | Critère | Preuve attendue |
|---|---|---|
| CA-01 | API accessible | Healthcheck HTTP |
| CA-02 | FIRMS collecté | lignes présentes en BDD |
| CA-03 | doublons maîtrisés | contrainte d'unicité |
| CA-04 | point géolocalisé | région associée |
| CA-05 | scoring | réponse du service ML ou fallback |
| CA-06 | clustering | FireEvent généré |
| CA-07 | statut | statut calculé |
| CA-08 | alerte | historique + retour provider |
| CA-09 | Chat | FastAPI → n8n → réponse |
| CA-10 | question métier | accès SQL aux données de feu |
| CA-11 | question documentaire | récupération Qdrant |
| CA-12 | frontend | carte/pages accessibles |
| CA-13 | deployment | Nginx + DuckDNS |
| CA-14 | SEO | sitemap/robots accessibles |
| CA-15 | sécurité | aucun secret dans Git/documentation |

---

## 19. RISQUES TECHNIQUES

| Risque | Conséquence | Réponse |
|---|---|---|
| FIRMS indisponible | pas de nouvelle collecte | logs + reprise du cycle |
| ML indisponible | score non disponible | fallback heuristique |
| GEE indisponible | enrichissement interrompu | traitement par lots/reprise |
| HDBSCAN indisponible | clustering différent | fallback grille |
| n8n indisponible | Chat indisponible | réponse de secours FastAPI |
| Qdrant indisponible | perte de contexte documentaire | conserver la séparation SQL/RAG |
| Provider SMS/WhatsApp indisponible | alerte non envoyée | statut d'échec + canal alternatif |
| erreur DNS/TLS | service inaccessible | validation Nginx/Certbot |
| mauvais domaine canonique | problème SEO | PRERENDER_BASE_URL cohérente |

---

## 20. LIMITES À NE PAS TRANSFORMER EN EXIGENCES RÉALISÉES

Les points suivants nécessitent une preuve indépendante avant d'être présentés comme fonctions pleinement opérationnelles :

1. une prédiction automatique systématique J+1 ;
2. une détection autonome complète de déforestation ;
3. une précision/accuracy scientifique provenant d'une valeur d'interface ;
4. un enrichissement GEE synchrone de chaque nouvelle observation du pipeline principal ;
5. une extinction physique certaine déduite uniquement de l'absence de détection ;
6. une configuration précise des nodes n8n non versionnés dans les dépôts étudiés.

---

## 21. TRAÇABILITÉ DU CODE

| Domaine | Fichier / dépôt de référence |
|---|---|
| Pipeline automatique | Backend/api/services/automatic_pipeline.py |
| FIRMS | Backend/api/services/firms_service.py |
| Géographie | Backend/api/services/geo_filter.py et region_label_service.py |
| ML | Backend/api/services/jerymotronet_service.py |
| Fallback | Backend/api/routers/internal.py |
| Clustering | Backend/api/services/cluster_service.py |
| Statut | Backend/api/services/fire_status_service.py |
| Alertes | Backend/api/services/alert_service.py |
| Chat | Backend/api/routers/chat.py et rag_service.py |
| GEE | Backend/data/gee_enrich_firms.py et Backend/data/GEE_ENRICH/main.py |
| Frontend | dépôt TkAbeleon/JeryMotro_WEB |
| Déploiement | conf.ngnix et scripts de déploiement |
| Données HF | rtsikynyantsa/MADAGASCAR_GEE_FIMRS |

---

## 22. DOCUMENTS LIÉS

- [[00_INDEX]]
- [[01_VISION_GENERALE]]
- [[03_ARCHITECTURE_TECHNIQUE]]
- [[04_PIPELINE_DONNEES]]
- [[07_ML_SCORING_RISQUE]]
- [[08_CLUSTERING_ET_SUIVI_DES_FEUX]]
- [[09_ENRICHISSEMENT_GEE_ENVIRONNEMENT]]
- [[11_ALERTES_ET_NOTIFICATIONS]]
- [[12_CHAT_IA_RAG]]
- [[16_DEPLOIEMENT_GCP_DEBIAN13]]
- [[17_HUGGING_FACE_DATA_ET_SCRIPTS]]
- [[18_NGINX_ET_ACCES_RESEAU]]
- [[21_STACK_TECHNIQUE]]
- [[22_PROTOCOLLES_ET_INTERFACES]]
- [[23_STRATEGIE_DEPLOIEMENT_DUCKDNS]]
- [[24_SEO_PRERENDER_SITEMAP_ROBOTS]]

---

## 23. POSITIONNEMENT

> **Le cahier des charges décrit à la fois le besoin fonctionnel et les contraintes techniques observées.**
>
> Pour la soutenance, il faut toujours distinguer **exigence**, **implémentation**, **intégration externe** et **fonction non démontrée**.

---

**Navigation :** [[24_SEO_PRERENDER_SITEMAP_ROBOTS|← Précédent]] | [[00_INDEX|Index]] | [[Glossaire_Tags|Glossaire →]]
