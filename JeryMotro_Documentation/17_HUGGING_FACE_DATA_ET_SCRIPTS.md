# Hugging Face, scripts et données

## 1. Rôle technique

Hugging Face intervient comme plateforme d'hébergement de datasets et comme cible de déploiement Docker pour certaines briques du projet.

Il faut distinguer :
- **Dataset Hub** : données ;
- **Space** : application/service ;
- **GitHub** : source du code.

## 2. Déploiement Space

Le workflow `.github/workflows/sync-to-huggingface.yml` :
1. se déclenche sur `main` ou manuellement ;
2. vérifie le Docker Space ;
3. vérifie `HF_SPACE_ID` ;
4. vérifie `HF_TOKEN` ;
5. installe `huggingface_hub` ;
6. crée/actualise le Space ;
7. upload le dépôt en excluant les secrets et fichiers locaux.

## 3. Port du Space

Le workflow vérifie que le README du Space déclare :
`sdk: docker`
et
`app_port: 7860`.

Le port 7860 est donc le port d'exposition du conteneur HF pour cette cible.

## 4. Secret HF_TOKEN

Le secret GitHub s'appelle `HF_TOKEN`.

Le dépôt ne révèle pas son scope exact. Il ne faut donc pas documenter un niveau de permission qui n'est pas observable dans le code.

## 5. Doppler

`HF_DEPLOY.md` documente un `DOPPLER_TOKEN` dans les secrets du Space.

Le démarrage peut passer par :

```
doppler run -- python /app/docker-entrypoint.py
```

Les credentials Google/GEE peuvent être reconstruits temporairement dans `/tmp`.

## 6. Exclusions de l'upload

Le workflow exclut notamment :
- `.env` ;
- `.env.*` ;
- bases de données ;
- SQLite ;
- logs ;
- .git ;
- certains artefacts de données.

## 7. Datasets

Le projet utilise notamment :
`rtsikynyantsa/MADAGASCAR_GEE_FIMRS`

Ce dataset contient des observations FIRMS accompagnées de variables de contexte environnemental.

Le dépôt contient aussi des jeux associés aux frontières et aux expérimentations de segmentation/UNet.

## 8. Scripts de calcul

Les scripts GEE utilisent notamment :
- pandas ;
- Earth Engine ;
- KaggleHub ;
- tqdm.

Ils fonctionnent par lots et écrivent des sorties enrichies.

## 9. Architecture de stockage

```
GitHub
  └─ code + scripts + docs

Hugging Face Dataset
  └─ données tabulaires / datasets

Hugging Face Space
  └─ service Docker

GCP
  └─ production multi-services + Nginx
```

## 10. Règle de preuve

La présence d'un dataset sur HF ne prouve pas qu'il est branché directement à la collecte FIRMS de production. La source d'une donnée doit être déterminée par le code du traitement concerné.