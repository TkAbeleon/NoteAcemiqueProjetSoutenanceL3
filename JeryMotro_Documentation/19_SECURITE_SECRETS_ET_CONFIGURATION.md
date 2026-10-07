# Sécurité, secrets et configuration

## Variables sensibles
La configuration backend prévoit notamment :
- `DATABASE_URL`
- `JWT_SECRET`
- `FIRMS_MAP_KEY`
- credentials GEE/Google
- `ML_SERVICE_API_KEY`
- webhooks n8n
- clé WAHA
- clés SMS.

Cette documentation cite uniquement les **noms de variables**, jamais leurs valeurs.

## GitHub Actions
Le workflow HF utilise `HF_SPACE_ID` et `HF_TOKEN`. Les valeurs et permissions détaillées des secrets ne sont pas visibles par le code du dépôt.

## Doppler
Le déploiement HF documenté utilise `DOPPLER_TOKEN`. Le document de déploiement décrit un token de service limité à la configuration Doppler utilisée.

## Credentials fichiers
Les fichiers Google/GEE sensibles peuvent être fournis sous forme encodée puis recréés au démarrage avec des permissions restrictives.

## .env
Le workflow GitHub → HF exclut les fichiers `.env` et les bases/logs locaux.

## CORS
FastAPI active CORS selon la configuration actuelle. Une politique de production plus restrictive peut être nécessaire selon le contexte.

## JWT côté navigateur
Le frontend conserve le JWT dans localStorage. Ce choix doit être pris en compte dans l'analyse de sécurité.

## Services externes
Chaque service possède ses propres mécanismes :
HTTPS/TLS, API keys, webhooks, credentials GEE, authentification SMSGate, etc.

## Règle absolue
> Ne jamais écrire une valeur réelle de secret dans une note, un commit, un diagramme ou une capture. Utiliser uniquement les noms de variables ou des placeholders.

---

**Navigation :** [[18_NGINX_ET_ACCES_RESEAU|← Précédent]] | [[00_INDEX|Index]] | [[20_LIMITES_ET_ETAT_REEL|Suivant →]]
