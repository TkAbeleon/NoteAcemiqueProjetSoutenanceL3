# 🔐 Accès Utilisateur — Sans inscription (sauf alertes)
#JeryMotro #MemoireL3 #Decision #Auth #Alerte #UX
[[Glossaire_Tags]] | [[00_INDEX]] | [[09_FastAPI_Backend]] | [[12_Systeme_Alertes]]

> Règle produit : **toutes les fonctionnalités sont accessibles sans inscription**, sauf la fonctionnalité **Alertes** qui nécessite une authentification.

---

## 1) Pourquoi l’authentification est nécessaire uniquement pour les alertes

Les alertes ont des risques spécifiques :
- coût potentiel (SMS) et abus (spam)
- données personnelles (numéro WhatsApp/SMS, email)
- besoin de traçabilité (qui a activé quoi, quand)

Donc : on garde le reste en “open access” pour la démo et l’UX, et on protège seulement la partie alertes.

---

## 2) Fonctionnalités disponibles sans inscription

- Consultation des détections : carte, filtres, historique
- Consultation des clusters / statut feu (inféré)
- Visualisation de la carte risque (si ConvLSTM)
- Dashboard statistiques (24h/semaine)
- Chat IA (si activé)

---

## 3) Fonctionnalité nécessitant authentification

### Alertes (auth obligatoire)
Canaux d’alerte :
- **Mail**
- **WhatsApp**
- **SMS**

Référence : [[12_Systeme_Alertes]].

Actions protégées :
- activer/désactiver les alertes
- enregistrer/modifier les destinations (email, numéros)
- consulter l’historique d’alertes d’un utilisateur

---

## 4) Spécification API (côté FastAPI)

### Endpoints publics (exemples)
- `GET /detections`
- `GET /clusters`
- `GET /risk-map`
- `POST /chat` (si tu le gardes public)

### Endpoints protégés (exemples)
- `POST /alerts/subscribe`
- `POST /alerts/unsubscribe`
- `GET /alerts/me`

> Mécanisme d’auth au choix (simple) : token/JWT géré par Supabase Auth, ou une clé API par utilisateur.

---

## 5) Données à stocker (BDD)

Minimum :
- `users` (ou table Supabase Auth) : `email`, `phone_number`, `whatsapp_number`, `created_at`
- `alert_subscriptions` : user_id, channel, destination (email/numéro), enabled, created_at
- `alerts` : user_id, detection_id/cluster/fire_id, message, status, sent_at

Objectif : audit + anti-spam + confidentialité.
