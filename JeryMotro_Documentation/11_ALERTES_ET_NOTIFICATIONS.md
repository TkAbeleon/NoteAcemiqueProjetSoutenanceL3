# Alertes et notifications

## Entités
Le backend possède notamment `Alert`, `AlertSubscription` et `MonitoredZone`.

## Abonnement
Un utilisateur peut configurer un canal et des seuils `min_risk` et `min_frp`. L'abonnement conserve notamment destination, activation et état de vérification.

## Rôles
Les canaux SMS et WhatsApp sont réservés aux rôles Premium et Admin par le routeur d'abonnement.

## OTP
Lorsqu'une nouvelle souscription doit être vérifiée :
- code à 6 chiffres ;
- expiration de 5 minutes ;
- compteur de tentatives remis à zéro.

Après trois erreurs, un nouveau code doit être demandé.

## Conditions
Une alerte est candidate si :
`risk_score >= min_risk` **ou** `frp >= min_frp`, sauf demande administrateur avec `force_send`.

## Canaux
- Email → webhook n8n ;
- WhatsApp → WAHA ;
- SMS → HTTPSMS ou SMSGate selon `SMS_PROVIDER`.

## Déclenchement automatique
Lors de la reconstruction des clusters, le backend peut évaluer automatiquement les abonnements et tenter les envois.

## Déclenchement manuel
Une route administrateur `/alerts/trigger` existe séparément.

## Limite
Le succès réel dépend des abonnements vérifiés, des seuils, des credentials et de la disponibilité des services externes.