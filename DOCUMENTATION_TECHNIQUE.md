# Documentation Technique Complète - Predictive Dialer Platform

**Projet:** Plateforme de Centre de Contact avec Predictive Dialer
**Stack:** Laravel 12 + Vue.js 3 + Node.js + Asterisk/FreePBX
**Date:** 2 Février 2026

---

## Table des matières

1. [Vue d'ensemble du projet](#1-vue-densemble-du-projet)
2. [Architecture globale](#2-architecture-globale)
3. [Outscaller - Application principale (Laravel + Vue.js)](#3-outscaller)
4. [Dialer Engine - Moteur d'appels (Node.js)](#4-dialer-engine)
5. [FreePBX CDR API - API de journaux d'appels](#5-freepbx-cdr-api)
6. [Communication inter-services](#6-communication-inter-services)
7. [Base de données et modèles](#7-base-de-données-et-modèles)
8. [Rôles utilisateurs et autorisations](#8-rôles-utilisateurs-et-autorisations)
9. [Guide d'installation](#9-guide-dinstallation)
10. [Variables d'environnement](#10-variables-denvironnement)
11. [Routes et API](#11-routes-et-api)
12. [Frontend Vue.js](#12-frontend-vuejs)
13. [Fonctionnalités métier](#13-fonctionnalités-métier)
14. [Déploiement](#14-déploiement)
15. [Troubleshooting](#15-troubleshooting)
16. [Conventions de code et ajout de fonctionnalités](#16-conventions-de-code)

---

## 1. Vue d'ensemble du projet

### Qu'est-ce que cette plateforme ?

C'est une plateforme de gestion de centre de contact composée de **3 services** :

| Service | Techno | Rôle |
|---------|--------|------|
| **outscaller** | Laravel 12 + Vue 3 + Inertia | Application web principale (UI, gestion leads, agents, campagnes) |
| **dialer-engine** | Node.js + TypeScript | Moteur de numérotation prédictive connecté à Asterisk via AMI |
| **freepbx-cdr** | Node.js + TypeScript + Express | API REST pour récupérer les CDR (Call Detail Records) de FreePBX |

### Diagramme de flux global

```
                    ┌─────────────────────────────────┐
                    │         NAVIGATEUR               │
                    │   Vue 3 + JSSIP (WebPhone)       │
                    │   + Laravel Echo (WebSocket)      │
                    └──────────┬──────────────────────┘
                               │ HTTP / WebSocket
                               ▼
┌──────────────────────────────────────────────────────┐
│                  OUTSCALLER (Laravel 12)              │
│  - Gestion utilisateurs (6 rôles)                     │
│  - Gestion leads & campagnes                          │
│  - Dashboards temps réel                              │
│  - Supervision agents                                 │
│  - Commissions & retraits                             │
│  - Formulaires dynamiques                             │
│  Port: 8000 (HTTP) + 8080 (Reverb WebSocket)          │
└────────┬─────────────────────┬───────────────────────┘
         │ Redis Pub/Sub       │ HTTP REST
         ▼                     ▼
┌─────────────────┐   ┌─────────────────────┐
│  DIALER ENGINE  │   │   FREEPBX CDR API   │
│  (Node.js)      │   │   (Node.js/Express)  │
│  - AMI Asterisk  │   │   - MySQL (cdr table)│
│  - Pacing algo   │   │   - GraphQL FreePBX  │
│  - Gestion appels│   │   - Auth API Key     │
│  Port: aucun     │   │   Port: 3000         │
└────────┬─────────┘   └──────────┬──────────┘
         │ AMI (TCP 5038)          │ MySQL/GraphQL
         ▼                         ▼
┌─────────────────────────────────────────────┐
│            ASTERISK / FREEPBX                │
│  - PBX SIP (5060/5061)                       │
│  - AMI (5038)                                │
│  - Enregistrement des appels                 │
│  - Queues d'agents                           │
└─────────────────────────────────────────────┘
```

---

## 2. Architecture globale

### Design Patterns communs aux 3 projets

Les 3 projets utilisent la **Clean Architecture** avec :

- **Repository Pattern** : Abstraction de l'accès aux données via interfaces
- **Service Layer** : Logique métier isolée dans des services
- **DTOs** : Objets de transfert de données pour la sécurité de type
- **Dependency Injection** : Injection de dépendances via containers IoC

### Technologies partagées

| Composant | Technologie |
|-----------|------------|
| Cache/Message Broker | **Redis** (partagé entre outscaller et dialer-engine) |
| Base de données principale | **MySQL** (outscaller + freepbx-cdr) |
| Temps réel | **Redis Pub/Sub** (commandes) + **Reverb** (WebSocket UI) |
| Téléphonie | **Asterisk/FreePBX** (PBX) + **Telnyx** (trunk SIP) |

---

## 3. Outscaller

### 3.1 Structure du projet

```
outscaller/
├── app/
│   ├── Console/Commands/         # Commandes artisan (FetchCdrs, SyncCdrs, etc.)
│   ├── Contracts/                # Interfaces (Repositories + Services)
│   │   ├── Repositories/         # 34+ interfaces de repositories
│   │   └── Services/             # 50+ interfaces de services
│   ├── DTOs/                     # Data Transfer Objects
│   ├── Events/                   # Événements Laravel (AgentStatusChanged, etc.)
│   ├── Factory/                  # Factories de création d'objets
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── Api/              # 6 controllers API
│   │   │   └── Web/
│   │   │       ├── Admin/        # 12 controllers admin
│   │   │       ├── Agent/        # 5 controllers agent
│   │   │       ├── Gerant/       # 7 controllers gérant
│   │   │       ├── ResponsablePlateau/   # 4 controllers
│   │   │       ├── ResponsableProjet/    # 3 controllers
│   │   │       ├── DO/           # 1 controller directeur opérationnel
│   │   │       ├── Common/       # 7 controllers partagés
│   │   │       └── Authentication/       # 2 controllers auth
│   │   ├── Middleware/           # CheckRole, Authenticate, etc.
│   │   ├── Requests/            # Form Requests (validation)
│   │   └── Resources/           # API Resources (serialization)
│   ├── Models/                  # 29 modèles Eloquent
│   ├── Providers/               # Service Providers (DI bindings)
│   ├── Repositories/Eloquent/   # 34+ implémentations repositories
│   ├── Services/                # 50+ services métier
│   └── Utils/                   # Enums, Constants, Helpers
├── database/migrations/         # 49 migrations
├── resources/js/                # Frontend Vue 3
│   ├── components/              # 100+ composants Vue
│   ├── pages/                   # Pages (admin, agent, gerant, etc.)
│   ├── stores/                  # Pinia stores
│   ├── plugins/                 # Axios, Echo, etc.
│   └── types/                   # Interfaces TypeScript
├── routes/
│   ├── web.php                  # Routes web (355 lignes)
│   ├── api.php                  # Routes API (77 lignes)
│   └── channels.php             # Channels WebSocket
└── config/                      # 17 fichiers de configuration
```

### 3.2 Stack technique

**Backend :**
- PHP 8.2 + Laravel 12
- Inertia.js 2.0 (pont Laravel <-> Vue)
- Sanctum (auth API)
- Reverb (WebSocket)
- Predis (client Redis)
- Telnyx PHP SDK (VoIP)
- Brevo PHP SDK (emails)

**Frontend :**
- Vue 3.5 + TypeScript
- Vite 7 (build)
- Tailwind CSS 4.1
- JSSIP 3.10 (WebRTC/SIP)
- Laravel Echo (WebSocket client)
- Pinia (state management)
- Chart.js (graphiques)

### 3.3 Couche Repository

Chaque entité suit le pattern : **Interface -> Implémentation Eloquent -> Service -> Controller**

```
Contracts/Repositories/LeadRepositoryInterface
         ↓
Repositories/Eloquent/LeadRepository
         ↓
Services/Lead/LeadService
         ↓
Http/Controllers/Web/Agent/AgentLeadController
```

Les bindings sont déclarés dans `RepositoryServiceProvider` et `AppServiceProvider` :

```php
// RepositoryServiceProvider.php
$this->app->bind(LeadRepositoryInterface::class, LeadRepository::class);
$this->app->bind(CallRepositoryInterface::class, CallRepository::class);
// ... 34+ bindings
```

### 3.4 Modèles principaux et relations

```
User ─────────────┬── AgentProfile ──── Trunk
                  ├── GerantProfile
                  ├── ResponsablePlateauxProfile ── Secteurs (M2M)
                  └── ResponsableProjetProfile ── Secteurs (M2M)

Lead ─── Secteur
     ─── AgentProfile
     ─── DynamicForm ─── FormField (HasMany)
     ─── FormSubmission
     ─── LeadComment (HasMany)
     ─── LeadValidationHistory (HasMany)
     ─── Call (HasMany)
     ─── Commission (HasMany)

Campaign ─── Secteur
         ─── Prospect (HasMany)

Team ─── Gerant (BelongsTo User)
     ─── TeamMember (HasMany) ─── User

Commission ─── Lead ─── AgentProfile
CommissionRule ─── Secteur
```

### 3.5 Services principaux

| Service | Fichier | Rôle |
|---------|---------|------|
| AuthenticationService | `Services/Authentication/` | Login, OTP 2FA, reset password |
| CallService | `Services/Call/CallService.php` | Gestion des appels VoIP (Telnyx) |
| TelnyxCallService | `Services/Call/TelnyxCallService.php` | Intégration API Telnyx |
| LeadService | `Services/Lead/LeadService.php` | CRUD leads, formulaires dynamiques |
| LeadValidationService | `Services/Lead/LeadValidationService.php` | Validation multi-niveaux |
| CampaignService | `Services/Campaign/CampaignService.php` | Gestion campagnes, Redis Pub/Sub |
| SupervisionService | `Services/Supervision/` | Monitoring temps réel agents |
| CommissionService | `Services/Remuneration/` | Calcul commissions |
| AdminDashboardService | `Services/Dashboard/` | Métriques globales |
| AgentDashboardService | `Services/Dashboard/` | Stats personnelles agent |
| CdrApiService | `Services/Cdrs/CdrApiService.php` | Intégration API CDR |
| BrevoMailService | `Services/Email/BrevoMailService.php` | Envoi emails via Brevo |

---

## 4. Dialer Engine

### 4.1 Structure du projet

```
dialer-engine/
├── src/
│   ├── main.ts                              # Point d'entrée, orchestrateur
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── Campaign.ts                  # Entité Campaign
│   │   │   └── Lead.ts                      # Entité Lead
│   │   ├── repositories/
│   │   │   └── IDialerRepository.ts         # Interface repo
│   │   └── services/
│   │       └── PacingAlgorithm.ts           # Algorithme de numérotation
│   ├── application/
│   │   ├── interfaces/
│   │   │   ├── IAmiClient.ts                # Interface AMI
│   │   │   └── IEventPublisher.ts           # Interface events
│   │   └── use-cases/
│   │       ├── ManageCampaignUseCase.ts     # Start/Stop/Pause campagnes
│   │       ├── DialingLoopUseCase.ts        # Boucle principale de numérotation
│   │       └── DialLeadUseCase.ts           # Originate un appel AMI
│   ├── interface-adapters/controllers/
│   │   ├── RedisCommandController.ts        # Écoute commandes Laravel
│   │   └── AmiEventController.ts            # Gestion events Asterisk
│   ├── infrastructure/
│   │   ├── ami/AmiClientWrapper.ts          # Client AMI Asterisk
│   │   ├── redis/
│   │   │   ├── RedisClientWrapper.ts        # Client Redis
│   │   │   └── RedisEventPublisher.ts       # Publication events
│   │   ├── repositories/
│   │   │   └── RedisDialerRepository.ts     # État dans Redis
│   │   └── config/Config.ts                 # Configuration
│   ├── utils/phoneNormalizer.ts             # Normalisation téléphone
│   └── types/asterisk-ami-client.d.ts       # Types AMI
├── scripts/verify_pacing.ts                 # Tests de l'algorithme
├── asterisk/extensions_custom.conf          # Dialplan Asterisk
├── Dockerfile
├── docker-compose.yml
├── package.json
└── .env.example
```

### 4.2 Stack technique

| Composant | Version | Usage |
|-----------|---------|-------|
| Node.js | 18 (Alpine) | Runtime |
| TypeScript | 5.4.5 | Typage |
| asterisk-ami-client | 1.1.5 | Protocole AMI |
| ioredis | 5.4.1 | Client Redis |
| tsyringe | 4.8.0 | Injection de dépendances |
| pino | 9.0.0 | Logging JSON |

### 4.3 Algorithme de Pacing (PacingAlgorithm.ts)

Le coeur du predictive dialer. Calcule combien d'appels lancer par cycle :

```
Mode Predictive:
  callsToPlace = (nombreAgents * dialingRatio) - canaux actifs
  callsToPlace = max(0, callsToPlace)

Exemple:
  10 agents × ratio 2.0 = 20 - 5 actifs = 15 appels à lancer

Mode Progressive:
  callsToPlace = nombreAgents - canaux actifs
```

### 4.4 Flux de la boucle de numérotation

```
1. DialingLoopUseCase exécuté toutes les 1000ms
2. Récupère le nombre d'agents prêts (Redis SCARD dialer:agents:ready)
3. Récupère le nombre d'appels actifs (Redis SCARD dialer:campaign:{id}:active_calls)
4. PacingAlgorithm calcule le nombre d'appels à lancer
5. Récupère N leads de la queue Redis (LPOP dialer:campaign:{id}:leads)
6. Pour chaque lead, exécute DialLeadUseCase:
   a. Envoie AMI Originate à Asterisk
   b. Stocke le mapping téléphone (Redis SET avec TTL 30min)
   c. Marque le lead comme DIALING
7. AmiEventController écoute les événements AMI:
   - DialBegin: Appel en cours
   - Bridge: Appel connecté (agent + client)
   - Hangup: Appel terminé, nettoyage Redis
```

### 4.5 Variables d'environnement

```bash
# Asterisk AMI
AMI_HOST=127.0.0.1
AMI_PORT=5038
AMI_USER=dialer
AMI_SECRET=your_secret

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=

# Dialer
DIALER_TRUNK=SIP/trunk_name
DIALER_ORIGINATE_CONTEXT=dialer-originate
DIALER_HANDLER_CONTEXT=dialer-queue-handler
DIALER_CALLER_ID=CompanyName
```

### 4.6 Déploiement Docker

```bash
docker build -t dialer-engine .
docker-compose up -d
```

Le `docker-compose.yml` inclut :
- dialer-engine (Node.js)
- redis (port 6380 externe)

---

## 5. FreePBX CDR API

### 5.1 Structure du projet

```
freepbx-cdr/
├── src/
│   ├── server.ts                              # Point d'entrée Express
│   ├── config/env.ts                          # Configuration
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── Cdr.ts                         # Entité CDR + CdrFilters
│   │   │   └── TokenResponse.ts               # Token OAuth
│   │   ├── repositories/
│   │   │   └── ICdrRepository.ts              # Interface
│   │   └── services/
│   │       └── LogService.ts                  # Logging JSON
│   ├── application/usecases/
│   │   ├── GetCdrsUseCase.ts                  # Récupération CDRs filtrés
│   │   └── GetCdrsByUniqueIdsUseCase.ts       # Récupération par IDs
│   ├── infrastructure/
│   │   ├── database/
│   │   │   ├── DataSource.ts                  # TypeORM config MySQL
│   │   │   └── entities/CdrEntity.ts          # Mapping table cdr
│   │   ├── http/
│   │   │   └── FreePBXClient.ts               # Client OAuth + GraphQL
│   │   └── repositories/
│   │       ├── MySQLCdrRepository.ts          # Accès direct MySQL
│   │       └── FreePBXCdrRepository.ts        # Via API GraphQL FreePBX
│   └── presentation/
│       ├── controllers/CdrController.ts       # Handlers HTTP
│       ├── middleware/AuthMiddleware.ts        # Auth Bearer token
│       └── routes/cdrRoutes.ts                # Routes Express
├── Makefile                                    # Déploiement PM2
├── package.json
└── tsconfig.json
```

### 5.2 Stack technique

| Composant | Version | Usage |
|-----------|---------|-------|
| Node.js | 20+ | Runtime |
| TypeScript | 5.9.3 | Typage |
| Express | 4.21.2 | Framework web |
| TypeORM | 0.3.28 | ORM MySQL |
| mysql2 | 3.15.3 | Driver MySQL |
| axios | 1.13.2 | Client HTTP (GraphQL FreePBX) |

### 5.3 Endpoints API

**Public :**
```
GET /health                     → { status: "ok", timestamp: "..." }
```

**Protégés (Bearer Token) :**
```
GET /api/cdrs                   → Liste CDRs avec filtres
GET /api/cdrs/batch             → CDRs par IDs uniques
```

**Paramètres de filtrage `/api/cdrs` :**

| Paramètre | Type | Description |
|-----------|------|-------------|
| extension | string | Filtre par extension (src/dst/cnum) |
| startDate | string | Date début (YYYY-MM-DD ou DD-MM-YYYY) |
| endDate | string | Date fin |
| minDuration | number | Durée minimum (secondes) |
| limit | number | Limite résultats (défaut 100) |
| orderBy | string | Champ de tri (défaut "calldate") |

**Exemple :**
```bash
curl -H "Authorization: Bearer <APP_SECRET>" \
  "http://localhost:3000/api/cdrs?extension=100&startDate=2025-11-05&minDuration=30&limit=50"
```

**Réponse :**
```json
{
  "success": true,
  "data": [
    {
      "id": "1234567890.123",
      "src": "100",
      "dst": "200",
      "cnum": "100",
      "duration": 120,
      "billsec": 115,
      "recordingfile": "/var/spool/asterisk/rec.wav",
      "calldate": "2025-02-02 14:30:45",
      "uniqueid": "1234567890.123"
    }
  ],
  "count": 1
}
```

### 5.4 Deux sources de données

Le projet supporte 2 implémentations interchangeables de `ICdrRepository` :

1. **MySQLCdrRepository** : Accès direct à la table `cdr` de MySQL (utilisé actuellement)
2. **FreePBXCdrRepository** : Via l'API GraphQL de FreePBX avec OAuth 2.0

La source active est définie dans `server.ts` :
```typescript
const cdrRepository = new MySQLCdrRepository();  // ← changer ici
```

### 5.5 Déploiement PM2

```bash
make deploy       # Déploiement complet (pull + build + restart PM2)
make quick-deploy # Mise à jour rapide
make status       # Voir statut PM2
make logs         # Voir les logs
make health-check # Test endpoint /health
```

---

## 6. Communication inter-services

### 6.1 Laravel <-> Dialer Engine (Redis Pub/Sub)

**Canal :** `dialer:commands`

| Action | Émetteur | Payload |
|--------|----------|---------|
| `START_CAMPAIGN` | Laravel | `{ campaign_id, mode, dialing_ratio }` |
| `PAUSE_CAMPAIGN` | Laravel | `{ campaign_id }` |
| `STOP_CAMPAIGN` | Laravel | `{ campaign_id }` |
| `CLEAR_ZOMBIES` | Laravel | `{ campaign_id }` |

**Clés Redis pour les données :**

| Clé | Type | Usage |
|-----|------|-------|
| `dialer:campaign:{id}:leads` | List | Queue FIFO des prospects à appeler |
| `dialer:agents:ready` | Set | Agents disponibles |
| `dialer:campaigns:active` | Hash | Campagnes actives |
| `dialer:campaign:{id}:active_calls` | Set | Appels en cours |
| `dialer:originate:phone:{number}` | String | Mapping téléphone -> prospect (TTL 30min) |

### 6.2 Laravel <-> FreePBX CDR API (HTTP REST)

```
Laravel (CdrApiService.php)
    │
    │ GET /api/cdrs?extension=XXX&startDate=...
    │ Authorization: Bearer <CDR_API_KEY>
    ▼
FreePBX CDR API (Express)
    │
    │ SELECT * FROM cdr WHERE ...
    ▼
MySQL (asteriskcdrdb.cdr)
```

Configuration dans outscaller `.env` :
```
CDR_API_BASE_URL=http://localhost:3000
CDR_API_KEY=Ch98rSFe14cD3jVtk69lPqP8RMVSYp0uP4Ml0aZ0Pg2mEfqBREZBLpoR3iFol7MI
```

### 6.3 Dialer Engine <-> Asterisk (AMI)

```
Dialer Engine
    │
    │ TCP 5038 (AMI Protocol)
    │ Action: Originate, Channel: SIP/trunk/number
    ▼
Asterisk PBX
    │
    │ Events: DialBegin, Bridge, BridgeEnter, Hangup, Rename
    ▼
Dialer Engine (AmiEventController)
    - Corrèle téléphones aux prospects
    - Détecte connexion agent-client
    - Nettoie les ressources au raccrochage
```

### 6.4 Frontend <-> Backend (WebSocket Reverb)

```
Vue 3 (Laravel Echo)
    │
    │ WebSocket ws://host:8080
    │ Channels: private-user.{id}, broadcast-supervision
    ▼
Laravel Reverb Server
    │
    │ Events: AgentStatusChanged, IncomingCallEvent, etc.
    ▼
Vue 3 (reactive UI updates)
```

---

## 7. Base de données et modèles

### 7.1 Base de données Outscaller (MySQL)

**49 migrations** couvrant :

| Groupe | Tables principales |
|--------|-------------------|
| Utilisateurs | `users`, `agent_profiles`, `gerant_profiles`, `responsable_plateaux_profiles`, `responsable_projet_profiles` |
| Appels | `calls`, `trunks` |
| Leads | `leads`, `lead_comments`, `lead_validation_history`, `form_submissions` |
| Formulaires | `dynamic_forms`, `form_fields` |
| Campagnes | `campaigns`, `prospects` |
| Organisation | `secteurs`, `teams`, `team_members`, `subsector_requests` |
| Commissions | `commissions`, `commission_rules`, `withdrawal_requests` |
| Auth | `otps`, `password_reset_tokens`, `personal_access_tokens` |
| Sessions | `agent_sessions`, `agent_pauses` |
| Docs | `documents`, `contact_messages` |

### 7.2 Table `leads` - Cycle de vie

```
NEW
  ↓ (Agent crée/saisit les données)
PENDING_AGENT
  ↓ (Superviseur qualité valide)
PENDING_PROJECT
  ↓ (Responsable projet approuve)
PENDING_ADMIN
  ↓ (Admin valide)
APPROVED  ──ou──  REJECTED (à n'importe quelle étape)
  ↓
CONVERTED (vente réalisée → commission calculée)
  ou CALLBACK (rappel nécessaire)
  ou INTERESTED (lead qualifié)
```

### 7.3 Table `campaigns` - Predictive Dialer

```sql
campaigns:
  id, secteur_id, name
  mode: predictive | progressive | preview
  status: draft | running | paused | completed | stopped
  dialing_ratio, queue_name
  timestamps, soft_deletes

prospects:
  id, campaign_id
  phone_number, first_name, last_name, email
  address, postal_code, city, country
  custom_fields (JSON)
  status: NEW | DIALING | LOCKED | CONVERTED | FAILED | DNC
  priority, locked_by_agent_id, locked_at
  timestamps
```

### 7.4 Base de données CDR (asteriskcdrdb)

```sql
cdr:
  uniqueid VARCHAR(32) PRIMARY KEY
  src VARCHAR(80)           -- Extension source
  dst VARCHAR(80)           -- Extension destination
  cnum VARCHAR(80)          -- Numéro appelant
  duration INT              -- Durée totale (secondes)
  billsec INT               -- Durée facturable
  recordingfile VARCHAR(255) -- Chemin enregistrement
  calldate DATETIME         -- Horodatage appel
```

---

## 8. Rôles utilisateurs et autorisations

### 6 rôles hiérarchiques

| Rôle | Préfixe route | Accès principal |
|------|--------------|----------------|
| **ADMIN** | `/admin/` | Accès total : utilisateurs, secteurs, campagnes, trunks, commissions, supervision |
| **DIRECTEUR_OPERATIONNEL (DO)** | `/do/` + `/admin/` | Dashboard opérationnel + accès admin partagé |
| **RESPONSABLE_PROJET** | `/responsable-projet/` | Validation leads, supervision secteurs assignés |
| **RESPONSABLE_PLATEAUX** | `/responsable-plateau/` | Supervision plateau, gestion équipes, commissions |
| **GERANT** | `/gerant/` | Gestion agents, équipes, leads, commissions, retraits |
| **AGENT** | `/agent/` | Création leads, appels (WebPhone), dialer, pauses |

### Middleware de vérification

```php
// routes/web.php
Route::middleware(['auth', 'role:admin,do'])->prefix('admin')->group(function () {
    // Routes admin...
});

Route::middleware(['auth', 'role:agent'])->prefix('agent')->group(function () {
    // Routes agent...
});
```

Le middleware `CheckRole` vérifie le rôle de l'utilisateur authentifié.

---

## 9. Guide d'installation

### 9.1 Prérequis

- PHP 8.2+ avec extensions : PDO, XML, cURL, Bcrypt, OpenSSL, Redis
- Node.js 18+ (dialer-engine) et 20+ (freepbx-cdr)
- MySQL 8.0+
- Redis 6.0+
- Asterisk/FreePBX (pour la téléphonie)
- Composer 2.x
- npm 9+

### 9.2 Installation Outscaller

```bash
cd outscaller
composer install
npm install
cp .env.example .env
php artisan key:generate

# Configurer .env (voir section 10)

php artisan migrate
npm run build              # Production
npm run dev                # Développement (hot reload)

# Démarrer les services
php artisan serve          # Serveur HTTP (port 8000)
php artisan reverb:start   # WebSocket (port 8080)
php artisan queue:listen   # Queue worker
```

### 9.3 Installation Dialer Engine

```bash
cd dialer-engine
npm install
cp .env.example .env

# Configurer .env (AMI, Redis)

npm run dev                # Développement (ts-node-dev)
npm run build && npm start # Production

# Ou via Docker
docker-compose up -d
```

### 9.4 Installation FreePBX CDR API

```bash
cd freepbx-cdr
npm install
cp .env.exemple .env

# Configurer .env (MySQL, APP_SECRET)

npm run dev                # Développement
npm run build && npm start # Production

# Ou via PM2
make setup                 # Configuration initiale PM2
make deploy                # Déploiement
```

---

## 10. Variables d'environnement

### 10.1 Outscaller (.env)

```bash
# === Application ===
APP_NAME=Outscaller
APP_ENV=local               # local|staging|production
APP_KEY=base64:...          # php artisan key:generate
APP_DEBUG=true
APP_URL=http://localhost:8000

# === Base de données ===
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=outscaller
DB_USERNAME=root
DB_PASSWORD=

# === Redis ===
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=null

# Redis séparé pour le dialer (optionnel)
DIALER_REDIS_HOST=127.0.0.1
DIALER_REDIS_PORT=6380

# === Cache & Session ===
CACHE_STORE=redis
SESSION_DRIVER=database

# === Queue ===
QUEUE_CONNECTION=database    # database|redis|sync

# === WebSocket (Reverb) ===
BROADCAST_CONNECTION=reverb
REVERB_APP_ID=123456
REVERB_APP_KEY=your_app_key
REVERB_APP_SECRET=your_app_secret
REVERB_HOST=localhost
REVERB_PORT=8080
REVERB_SCHEME=http

VITE_REVERB_APP_KEY=${REVERB_APP_KEY}
VITE_REVERB_HOST=${REVERB_HOST}
VITE_REVERB_PORT=${REVERB_PORT}
VITE_REVERB_SCHEME=${REVERB_SCHEME}

# === Téléphonie Telnyx ===
TELNYX_API_KEY=KEY0199A3CB...
TELNYX_PUBLIC_KEY=Z1xj09sTWnU6...
TELNYX_SIP_USERNAME=usercontact95342
TELNYX_SIP_PASSWORD=...
TELNYX_CONNECTION_ID=2796528457968781170

# === Email Brevo ===
BREVO_API_KEY=xkeysib-...
BREVO_FROM_ADDRESS=noreply@outscaller.com

# === CDR API ===
CDR_API_BASE_URL=http://localhost:3000
CDR_API_KEY=Ch98rSFe14cD3jVtk69l...
CDR_API_TIMEOUT=30

# === FreePBX ===
FREEPBX_RECORDING_BASE_URL=https://voip.outscaller.com
```

### 10.2 Dialer Engine (.env)

```bash
AMI_HOST=127.0.0.1
AMI_PORT=5038
AMI_USER=dialer
AMI_SECRET=your_ami_secret

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=

DIALER_TRUNK=SIP/trunk_name
DIALER_ORIGINATE_CONTEXT=dialer-originate
DIALER_HANDLER_CONTEXT=dialer-queue-handler
DIALER_CALLER_ID=CompanyName

NODE_ENV=production
LOG_LEVEL=info
```

### 10.3 FreePBX CDR API (.env)

```bash
APP_NAME=freepbx-cdr-api
APP_PORT=3000
APP_SECRET=<clé_API_forte>

FREEPBX_BASE_URL=https://voip.outscaller.com
FREEPBX_CLIENT_ID=<oauth_client_id>
FREEPBX_CLIENT_SECRET=<oauth_client_secret>
FREEPBX_SCOPE=gql:cdr

DB_HOST=voip.outscaller.com
DB_PORT=3306
DB_USER=cdr_reader
DB_PASSWORD=<mot_de_passe_db>
DB_NAME=asteriskcdrdb
```

---

## 11. Routes et API

### 11.1 Routes principales par rôle (outscaller)

**Authentification (public) :**
```
POST /auth/authenticate          # Login (rate-limited 5/min)
POST /auth/validate-otp          # Validation OTP 2FA
POST /auth/forgot-password       # Demande reset password
POST /auth/reset-password        # Reset password
```

**Admin :**
```
GET    /admin/dashboard
GET    /admin/users               # Liste utilisateurs
POST   /admin/users               # Créer utilisateur
GET    /admin/leads               # Tous les leads
GET    /admin/supervision         # Supervision temps réel
GET    /admin/campaigns           # Campagnes predictive
POST   /admin/campaigns/{id}/start|pause|stop
GET    /admin/trunk               # Trunks VoIP
GET    /admin/sectors             # Secteurs
```

**Agent :**
```
GET    /agent/dashboard
GET    /agent/lead                # Mes leads
POST   /agent/lead                # Créer lead
GET    /agent/calls               # Historique appels
POST   /agent/call/initiate       # Lancer appel
PUT    /agent/call/{id}/hangup    # Raccrocher
POST   /agent/pause/start|end     # Gestion pauses
GET    /agent/predictive           # Interface dialer
```

**Gérant :**
```
GET    /gerant/dashboard
GET    /gerant/users              # Mes agents
GET    /gerant/team               # Mes équipes
GET    /gerant/leads              # Leads équipe
GET    /gerant/supervision        # Supervision agents
GET    /gerant/commissions        # Commissions
POST   /gerant/withdrawal/request # Demande retrait
```

### 11.2 Routes API (api.php)

```
# Agent Status
POST   /api/agent/status          # Mettre à jour statut agent
GET    /api/agent/statuses        # Liste statuts agents

# Campagnes
GET    /api/campaigns/            # Liste campagnes
POST   /api/campaigns/{id}/start|pause|stop
POST   /api/campaigns/{id}/clear-zombies

# Prospects
GET    /api/prospects/search      # Recherche prospect
POST   /api/prospects/{id}/outcome # Enregistrer résultat appel

# Predictive
POST   /api/predictive/call/accept|reject|end
```

---

## 12. Frontend Vue.js

### 12.1 Structure des pages

```
resources/js/pages/
├── admin/
│   ├── Dashboard.vue         # KPIs globaux, graphiques
│   ├── Users.vue             # CRUD utilisateurs
│   ├── Leads.vue             # Gestion leads
│   ├── Campaigns.vue         # Gestion campagnes
│   ├── Supervision.vue       # Monitoring agents
│   ├── Sectors.vue           # Configuration secteurs
│   ├── Trunks.vue            # Gestion trunks VoIP
│   ├── CommissionRules.vue   # Règles commissions
│   └── WithdrawalManagement.vue
├── agent/
│   ├── Dashboard.vue         # Stats personnelles
│   ├── Call.vue              # WebPhone + Dialpad
│   ├── Leads.vue             # Mes leads
│   └── Predictive.vue        # Interface dialer prédictif
├── gerant/
│   ├── Dashboard.vue
│   ├── Users.vue
│   ├── Teams.vue
│   ├── Supervision.vue
│   ├── Commission.vue
│   └── Withdrawal.vue
├── auth/
│   ├── Login.vue
│   ├── VerifyOtp.vue
│   ├── ForgotPassword.vue
│   └── ResetPassword.vue
└── home/                     # Pages marketing publiques
    ├── Index.vue
    ├── Contact.vue
    └── Solutions.vue
```

### 12.2 Composants clés

**WebPhone (agent/Call.vue) :**
- Utilise JSSIP pour les appels SIP/WebRTC
- Dialpad complet avec actions (mute, hold, transfer)
- Détection d'appels entrants du dialer prédictif
- Pop-up automatique fiche prospect
- Historique des appels

**Supervision (admin/Supervision.vue) :**
- Liste agents en temps réel (via Reverb)
- Statut : En ligne / En appel / En pause / Hors ligne
- Métriques par agent (appels, conversions, durée)

**Campaign management :**
- `resources/js/pages/admin/campaign/Index.vue` - Liste campagnes
- `resources/js/pages/admin/campaign/Create.vue` - Création
- `resources/js/pages/admin/campaign/Show.vue` - Détail + upload CSV + contrôles

### 12.3 State Management (Pinia)

```typescript
// stores/call.ts
activeCall: Call | null
recentCalls: Call[]
callStatus: 'idle' | 'ringing' | 'connected' | 'ended'

// stores/auth.ts
user: User | null
isAuthenticated: boolean
role: UserRole

// stores/campaign.ts
activeCampaign: Campaign | null
campaignStats: Stats
prospects: Prospect[]
```

### 12.4 WebSocket (Laravel Echo)

Configuré dans `resources/js/plugins/echo.ts` :

```typescript
import Echo from 'laravel-echo'
import Pusher from 'pusher-js'

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT,
    forceTLS: false,
})
```

---

## 13. Fonctionnalités métier

### 13.1 Gestion des leads

1. **Création** : L'agent remplit un formulaire dynamique (configurable par secteur)
2. **Validation multi-niveaux** : Agent -> Qualité -> Projet -> Admin
3. **Suivi** : Commentaires, historique de validation, pièces jointes
4. **Conversion** : Lead APPROVED -> CONVERTED (vente) -> Commission calculée

### 13.2 Système d'appels

- **Manuel** : L'agent compose un numéro via le WebPhone (JSSIP)
- **Prédictif** : Le dialer-engine lance les appels et connecte aux agents
- **CDR** : Les enregistrements sont synchronisés depuis FreePBX via la CDR API

### 13.3 Campagnes prédictives

1. Admin crée une campagne (mode, ratio, secteur)
2. Upload CSV de prospects
3. Démarre la campagne (Redis Pub/Sub -> dialer-engine)
4. Le dialer-engine appelle les prospects automatiquement
5. Connexion agent-client via queue Asterisk
6. L'agent enregistre le résultat (intéressé, rappel, refus, etc.)

### 13.4 Commissions

- Règles configurables par secteur (fixe, pourcentage, progressif)
- Calcul automatique à la conversion d'un lead
- Suivi des gains par agent et gérant
- Système de retrait (demande -> approbation admin -> paiement)

### 13.5 Supervision temps réel

- Statut agents en temps réel (WebSocket)
- Métriques : appels en cours, taux de conversion, durée moyenne
- Détection d'anomalies (agents inactifs, appels trop longs)
- Disponible pour Admin, DO, Gérant, Responsable Plateau/Projet

### 13.6 Pauses agents

Types : Pause, Déjeuner, Admin, Formation, Autre
- Suivi de la durée de chaque pause
- Statistiques par type
- L'agent est marqué indisponible pendant la pause

---

## 14. Déploiement

### 14.1 Outscaller

```bash
# Via Makefile
make deploy

# Manuel
git pull origin develop
composer install --optimize-autoloader --no-dev
npm install && npm run build
php artisan migrate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan storage:link
php artisan reverb:start &     # WebSocket
php artisan queue:listen &     # Queue worker
```

### 14.2 Dialer Engine

```bash
# Via Docker
docker build -t dialer-engine .
docker-compose up -d

# Manuel
npm install
npm run build
node dist/main.js
```

### 14.3 FreePBX CDR API

```bash
# Via PM2
make deploy                    # Full deploy (git pull + build + PM2 restart)
make quick-deploy              # Quick update

# Manuel
npm install
npm run build
pm2 start dist/server.js --name freepbx-cdr-api
```

### 14.4 Services à démarrer

| Service | Commande | Port |
|---------|----------|------|
| Outscaller (HTTP) | `php artisan serve` | 8000 |
| Outscaller (WebSocket) | `php artisan reverb:start` | 8080 |
| Outscaller (Queue) | `php artisan queue:listen` | - |
| Dialer Engine | `docker-compose up -d` | - |
| FreePBX CDR API | `pm2 start freepbx-cdr-api` | 3000 |
| Redis | Service système | 6379/6380 |
| MySQL | Service système | 3306 |
| Asterisk | Service système | 5038/5060 |

---

## 15. Troubleshooting

### Problèmes courants

**WebSocket ne se connecte pas :**
- Vérifier que Reverb tourne : `php artisan reverb:start`
- Vérifier REVERB_HOST/PORT dans `.env`
- Vérifier VITE_REVERB_* dans `.env` et rebuild frontend

**Dialer Engine ne se connecte pas à Asterisk :**
- Vérifier qu'Asterisk est lancé : `asterisk -r`
- Vérifier AMI_HOST, AMI_PORT, AMI_USER, AMI_SECRET
- Vérifier `/etc/asterisk/manager.conf` (permissions AMI)
- Note : le dialer continue sans AMI (mode dégradé)

**CDR API erreur 401/403 :**
- Vérifier le header `Authorization: Bearer <APP_SECRET>`
- Vérifier que `APP_SECRET` est défini dans `.env` de freepbx-cdr

**Redis ne se connecte pas :**
- Vérifier Redis : `redis-cli ping` -> `PONG`
- Vérifier REDIS_HOST/PORT dans `.env`
- Vérifier le mot de passe Redis si défini

**Pas de leads dans la queue Redis :**
- Vérifier : `redis-cli LLEN dialer:campaign:1:leads`
- Vérifier que Laravel a bien pushé les leads
- Vérifier le format JSON des leads

**Phone mapping NOT FOUND (dialer-engine) :**
- Vérifier la normalisation du numéro de téléphone
- Vérifier le TTL (30 minutes)
- Inspecter : `redis-cli KEYS 'dialer:originate:phone:*'`

### Commandes de debug

```bash
# Redis
redis-cli KEYS 'dialer:*'
redis-cli SCARD dialer:agents:ready
redis-cli LLEN dialer:campaign:1:leads
redis-cli HGETALL dialer:campaigns:active

# Asterisk
asterisk -rx "core show channels"
asterisk -rx "queue show 400"
asterisk -rx "manager show users"

# Laravel
php artisan tinker
>>> DB::connection()->getPdo()
>>> User::count()

# Logs
tail -f storage/logs/laravel.log          # Outscaller
docker logs dialer-engine                  # Dialer
pm2 logs freepbx-cdr-api                  # CDR API
```

---

## 16. Conventions de code

### 16.1 Ajouter une nouvelle fonctionnalité (Outscaller)

Suivre l'ordre :

1. **Migration** : `php artisan make:migration create_xxx_table`
2. **Modèle** : `app/Models/Xxx.php` avec relations Eloquent
3. **Interface Repository** : `app/Contracts/Repositories/XxxRepositoryInterface.php`
4. **Implémentation Repository** : `app/Repositories/Eloquent/XxxRepository.php`
5. **DTO** : `app/DTOs/Xxx/CreateXxxDTO.php`
6. **Interface Service** : `app/Contracts/Services/XxxServiceInterface.php`
7. **Service** : `app/Services/Xxx/XxxService.php`
8. **Binding** : Ajouter dans `RepositoryServiceProvider` et `AppServiceProvider`
9. **Form Request** : `app/Http/Requests/Xxx/CreateXxxRequest.php`
10. **Controller** : `app/Http/Controllers/Web/{Role}/XxxController.php`
11. **Route** : Ajouter dans `routes/web.php`
12. **Page Vue** : `resources/js/pages/{role}/Xxx.vue`
13. **Tests** : `tests/Unit/` et `tests/Feature/`

### 16.2 Standards de code

- **PHP** : PSR-12, Laravel Pint (`vendor/bin/pint`)
- **TypeScript/Vue** : ESLint + Prettier
- **Nommage** :
  - Controllers : `{Role}{Entite}Controller` (ex: `AdminLeadController`)
  - Services : `{Entite}Service` (ex: `LeadService`)
  - Repositories : `{Entite}Repository` (ex: `LeadRepository`)
  - DTOs : `{Action}{Entite}DTO` (ex: `CreateLeadDTO`)
  - Pages Vue : `{role}/{Entite}.vue` (ex: `admin/Leads.vue`)

### 16.3 Dialer Engine - Conventions

- Clean Architecture stricte : domain -> application -> infrastructure
- Injection de dépendances via `tsyringe` (`@injectable()`, `@inject()`)
- Interfaces préfixées par `I` (ex: `IAmiClient`, `IDialerRepository`)
- Use Cases : un use case = une action métier

### 16.4 FreePBX CDR API - Conventions

- Clean Architecture : domain -> application -> infrastructure -> presentation
- DI manuelle dans `server.ts`
- Logging via `LogService` (statique, JSON format)
- Auth : Bearer token statique (APP_SECRET)

---

## Annexe : Résumé des fichiers clés

### Outscaller

| Fichier | Rôle |
|---------|------|
| `routes/web.php` | Toutes les routes web (355 lignes) |
| `routes/api.php` | Routes API (77 lignes) |
| `app/Providers/RepositoryServiceProvider.php` | Bindings repositories |
| `app/Providers/AppServiceProvider.php` | Bindings services |
| `app/Http/Middleware/CheckRole.php` | Vérification rôle utilisateur |
| `app/Services/Campaign/CampaignService.php` | Logique campagnes + Redis |
| `app/Services/Call/CallService.php` | Logique appels + Telnyx |
| `app/Services/Lead/LeadService.php` | Logique leads |
| `config/services.php` | Config Telnyx, Brevo, CDR API |
| `resources/js/plugins/echo.ts` | Configuration WebSocket |

### Dialer Engine

| Fichier | Rôle |
|---------|------|
| `src/main.ts` | Orchestrateur, initialise tout |
| `src/domain/services/PacingAlgorithm.ts` | Algorithme de pacing |
| `src/application/use-cases/DialingLoopUseCase.ts` | Boucle principale |
| `src/application/use-cases/DialLeadUseCase.ts` | Lance un appel AMI |
| `src/interface-adapters/controllers/RedisCommandController.ts` | Écoute commandes |
| `src/interface-adapters/controllers/AmiEventController.ts` | Events Asterisk |
| `src/infrastructure/repositories/RedisDialerRepository.ts` | État Redis |
| `src/utils/phoneNormalizer.ts` | Normalisation numéros |

### FreePBX CDR API

| Fichier | Rôle |
|---------|------|
| `src/server.ts` | Point d'entrée Express |
| `src/infrastructure/repositories/MySQLCdrRepository.ts` | Accès MySQL |
| `src/infrastructure/http/FreePBXClient.ts` | Client OAuth/GraphQL |
| `src/presentation/controllers/CdrController.ts` | Handlers HTTP |
| `src/presentation/middleware/AuthMiddleware.ts` | Auth Bearer token |
| `Makefile` | Déploiement PM2 |
