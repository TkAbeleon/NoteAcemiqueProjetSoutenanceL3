# ⚙️ Automatisation n8n — JeryMotro Platform
#JeryMotro #MemoireL3 #n8n #Workflow #API #Alerte
[[Glossaire_Tags]] | [[00_INDEX]] | [[02_Architecture_Globale]]

---

## 1. WORKFLOWS PRINCIPAUX

| Workflow | Déclencheur | Actions | Fichier |
|----------|-------------|---------|---------|
| `daily_collection` | CRON `*/30 * * * *` | Fetch FIRMS → Preprocess → BDD | `n8n/workflows/daily_collection.json` |
| `alert_trigger` | Appelé après inférence | IF score>0.7 → Email + WhatsApp | `n8n/workflows/alert_trigger.json` |
| `weekly_report` | CRON `0 8 * * 1` | Agrégat → PDF → Email | `n8n/workflows/weekly_report.json` |

---

## 2. WORKFLOW daily_collection

```
[CRON : */30 * * * *]
    │
    ├─→ [HTTP Request : VIIRS_SNPP_NRT]
    │       URL : /api/area/csv/KEY/VIIRS_SNPP_NRT/-25.5,43,-11.5,50/1
    ├─→ [HTTP Request : VIIRS_NOAA21_NRT]
    └─→ [HTTP Request : MODIS_NRT]
    │
    ↓
[Code Node : fusion + déduplication]
    ↓
[Execute Command : python fetch_firms.py --merge]
    ↓
[Execute Command : python clean_firms.py]
    ↓
[Execute Command : python feature_engineering.py]
    ↓
[Execute Command : python hdbscan_cluster.py]
    ↓
[Execute Command : python run_madfirenet.py]
    ↓
[HTTP Request : POST http://madfire-api:8000/internal/save-results]
    ↓
[IF : any(risk_score > 0.7) OR any(frp > 50)]
    ↓ YES
[Trigger webhook : alert_trigger]
```

---

## 3. WORKFLOW alert_trigger

```
[Webhook Trigger]
    ↓
[Code Node : extraire zones à risque + construire message]
    ↓
[n8n Twilio Node]
    → To: whatsapp:+VOTRE_NUMERO
    → From: whatsapp:+14155238886 (Twilio sandbox)
    → Message: "🔥 ALERTE MADFIRE : {n} zones à risque élevé. FRP max : {frp}MW..."
    ↓
[Send Email Node]
    → To: alertes@votremail.com
    → Subject: "[ALERTE] JeryMotro - {date} - {n} clusters critiques"
    ↓
[HTTP Request : POST /alerts (FastAPI) → enregistrer en BDD]
```

---

## 4. n8n via Docker

n8n est inclus dans le `docker-compose.yml` → [[08_Docker_Infrastructure]].
- Accès : http://localhost:5678
- Importer les workflows depuis `n8n/workflows/*.json`
- Configurer les credentials (FIRMS MAP_KEY, Email, Twilio) dans Settings > Credentials

---

*Architecture → [[02_Architecture_Globale]]*
*Alertes → [[12_Systeme_Alertes]]*
