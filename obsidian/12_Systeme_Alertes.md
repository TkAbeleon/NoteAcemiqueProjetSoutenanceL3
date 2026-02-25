# 🔔 Système d'Alertes — JeryMotro Platform
#JeryMotro #MemoireL3 #Alerte #API #Python
[[Glossaire_Tags]] | [[00_INDEX]] | [[11_Automatisation_n8n]]

---

## Déclencheurs d'Alerte

| Condition | Niveau | Action |
|-----------|--------|--------|
| `risk_score > 0.70` | 🟠 ÉLEVÉ | Email + WhatsApp |
| `frp > 50 MW` | 🔴 CRITIQUE | Email + WhatsApp immédiat |
| `cluster_size ≥ 10 points` | 🔴 CRITIQUE | Email + WhatsApp |
| `risk_score > 0.50` | 🟡 MODÉRÉ | Email uniquement |

---

## Service Alertes (Python)

```python
# api/services/alert_service.py
import smtplib, os
from email.mime.text import MIMEText
from twilio.rest import Client

def send_whatsapp_alert(message: str):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        body=message,
        from_="whatsapp:+14155238886",   # Twilio Sandbox
        to=f"whatsapp:{os.getenv('ALERT_PHONE')}"
    )

def send_email_alert(subject: str, body: str):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = "madfire@gmail.com"
    msg['To'] = os.getenv("ALERT_EMAIL")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("madfire@gmail.com", os.getenv("SMTP_PASSWORD"))
        smtp.send_message(msg)

def trigger_alert_if_needed(risk_score: float, frp: float, region: str, date: str):
    if risk_score > 0.70 or frp > 50:
        message = f"🔥 ALERTE MADFIRE {date}\nRégion : {region}\nFRP : {frp}MW | Risque : {risk_score:.0%}"
        send_whatsapp_alert(message)
        send_email_alert(f"[ALERTE] JeryMotro {date}", f"<h2>{message}</h2>")
```

---

## Template Message WhatsApp

```
🔥 *ALERTE MADFIRE* — {date}

📍 *Région :* {region}
🌡️ *FRP max :* {frp} MW
⚠️ *Score risque :* {score}%
🔢 *Clusters actifs :* {n_clusters}

👉 Dashboard : http://localhost:3000
```

---

*n8n → [[11_Automatisation_n8n]]*
*FastAPI → [[09_FastAPI_Backend]]*
