# Hugging Face, scripts et données

## Rôle
Hugging Face est utilisé dans le projet pour :
- des datasets ;
- un Docker Space de déploiement ;
- des environnements de service/ML selon la configuration.

## GitHub → Hugging Face
Le workflow :
`.github/workflows/sync-to-huggingface.yml`

se déclenche sur `main` ou manuellement.

Il vérifie notamment Dockerfile, `docker-entrypoint.py`, requirements, le mode Docker et le port 7860.

## Secrets du workflow
Le workflow utilise :
- `HF_SPACE_ID` comme variable de repository ;
- `HF_TOKEN` comme secret GitHub.

**Le scope exact de HF_TOKEN n'est pas visible dans le dépôt**. Il ne faut pas l'inventer.

## Exclusions
L'upload exclut notamment :
- `.env` ;
- bases SQLite/DB ;
- logs ;
- métadonnées Git.

## Doppler
`HF_DEPLOY.md` indique l'utilisation de `DOPPLER_TOKEN` dans le Space et un démarrage via Doppler. Les credentials Google/GEE peuvent être reconstruits à l'exécution dans `/tmp`.

## Dataset
Le projet utilise notamment :
`rtsikynyantsa/MADAGASCAR_GEE_FIMRS`

La page Hugging Face correspond à un dataset tabulaire FIRMS enrichi de variables environnementales.

## Distinctions
- GitHub : code et documentation.
- Hugging Face Dataset : jeux de données.
- Hugging Face Space : application/service Docker.
- GCP : infrastructure d'exécution et reverse proxy.

## Attention
Un dataset présent sur Hugging Face n'est pas automatiquement une preuve qu'il alimente directement le pipeline FastAPI actuel.