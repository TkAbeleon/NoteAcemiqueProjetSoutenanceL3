# 🏗️ Conception UML — Backend FastAPI
#JeryMotro #MemoireL3 #UML #FastAPI #Backend
[[Glossaire_Tags]] | [[00_INDEX]] | [[09_FastAPI_Backend]] | [[02_Architecture_Globale]]

---

> Ce document présente la modélisation UML simplifiée du backend **FastAPI** pour la plateforme JeryMotro. Il définit l'architecture des composants, les modèles de données, et le flux d'exécution.

---

## 1. Diagramme de Composants (Architecture en Couches)

Ce diagramme montre l'organisation interne de l'application FastAPI. Les requêtes entrent par les routeurs (`Routers`), sont traitées par la logique métier (`Services`), puis interagissent avec la base de données via l'ORM (`SQLAlchemy`).

```mermaid
graph TD
    subgraph "🚀 FastAPI Application"
        A[main.py<br/>Point d'entrée & CORS] --> B(Routers<br/>Endpoints API)
        
        B --> |/api/detections| C1[routers/detections.py]
        B --> |/api/predictions| C2[routers/predictions.py]
        B --> |/api/chat| C3[routers/chat.py]
        B --> |/api/alerts| C4[routers/alerts.py]
        
        C1 --> D1[services/madfirenet_service.py]
        C2 --> D1
        C3 --> D2[services/rag_service.py]
        C4 --> D3[services/alert_service.py]
        
        D1 --> E[database.py<br/>SQLAlchemy ORM]
        D2 --> E
        D3 --> E
    end
    
    E -->|Lecture / Écriture| F[(🐘 PostgreSQL<br/>Supabase)]
    D2 -.->|Recherche Sémantique| G[(🧠 ChromaDB<br/>Base Vectorielle)]
```

---

## 2. Diagramme de Classes (Modèles BDD)

Ce diagramme UML représente les entités principales de la base de données PostgreSQL gérées par SQLAlchemy, ainsi que leurs relations.

```mermaid
classDiagram
    class Detection {
        +Integer id
        +String source
        +Float latitude
        +Float longitude
        +DateTime acq_datetime
        +Float frp
        +String satellite
        +Float risk_score
        +String niveau_risque
    }

    class Cluster {
        +Integer id
        +Integer cluster_size
        +Float frp_total
        +Float frp_max
        +DateTime date
        +Float center_lat
        +Float center_lon
    }

    class Alert {
        +Integer id
        +Integer detection_id
        +String message
        +String status
        +DateTime sent_at
        +DateTime created_at
    }

    class User {
        +Integer id
        +String name
        +String email
        +String phone
        +DateTime created_at
    }

    Cluster "1" -- "0..*" Detection : Contient
    Detection "1" -- "0..1" Alert : Déclenche
    User "1" -- "0..*" Alert : Reçoit
```

---

## 3. Diagramme de Séquence (Flux d'Inférence & Alerte)

Ce diagramme illustre ce qui se passe dans le backend lorsqu'une nouvelle donnée FIRMS est reçue (généralement poussée par le workflow `n8n`).

```mermaid
sequenceDiagram
    autonumber
    actor n8n as n8n (CRON 30m)
    participant API as FastAPI (Router)
    participant ML as MadFireNet Service
    participant DB as Supabase (PostgreSQL)
    participant Alert as Alert Service
    participant LLM as Groq (Llama-3)

    n8n->>API: POST /api/detections (Données brutes)
    activate API
    API->>ML: enrich_and_predict(data)
    activate ML
    ML-->>ML: Extraction GEE (Météo, Pente, NDVI)
    ML-->>ML: Inférence XGBoost -> risk_score
    ML-->>API: Résultat (risk_score, niveau_risque)
    deactivate ML
    
    API->>DB: INSERT INTO detections
    
    alt risk_score > 0.70 ou FRP > 50
        API->>Alert: trigger_alert(detection)
        activate Alert
        Alert->>Alert: Générer PNG (Thermique/Visible)
        Alert-->>n8n: (Webhook SMS/WhatsApp)
        deactivate Alert
    end
    
    API-->>n8n: 201 Created (Success)
    deactivate API

    note over API,LLM: Cas d'usage : Utilisateur pose une question
    actor User as Dashboard (React)
    User->>API: POST /api/chat {question}
    API->>LLM: Générer réponse avec Contexte (RAG)
    LLM-->>API: Réponse texte
    API-->>User: Affichage Assistant
```

---

*Fichier généré pour servir de base au développement du backend (Semaines 7-8).*
