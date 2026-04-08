# 📋 Cahier des Charges — FireProject
#FireProject #MemoireL3 #ThinkTank #Soutenance
[[Glossaire_Tags]] | [[00_INDEX]]

---

## 1. IDENTIFICATION DU PROJET

| Champ                | Détail                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------- |
| **Titre**            | Plateforme intelligente de suivi des feux de brousse et de la déforestation à Madagascar |
| **Niveau**           | Mémoire de Licence L3                                                                    |
| **Encadrante**       | RANDRIAMIARISON Zilga Heritiana                                                          |
| **Type**             | Projet technologique                                                                     |
| **Date de début**    | Février 2026                                                                             |
| **Soutenance cible** | Mai 2026                                                                                 |
| **Budget initial**   | 0 Ar (phase prototype)                                                                   |

---

## 2. CONTEXTE ET PROBLÉMATIQUE

### 2.1 Contexte environnemental

Madagascar est l'un des pays les plus touchés par la déforestation en Afrique. Chaque année :
- Des milliers d'hectares de forêt disparaissent à cause des feux de brousse
- La déforestation progresse à un rythme alarmant (perte de biodiversité unique)
- Les communautés rurales sont directement impactées (sols dégradés, risques sanitaires)

### 2.2 Problème technique central

> Les données satellites existent (NASA, ESA) mais il manque une **chaîne intelligente locale** pour les transformer en décisions.

**Trois lacunes majeures identifiées :**

| # | Lacune | Impact |
|---|--------|--------|
| 1 | Données dispersées et non automatisées | Aucune veille systématique |
| 2 | Données non interprétées localement | Décideurs sans information claire |
| 3 | Absence d'anticipation ML/DL | Réaction tardive aux incendies |

### 2.3 Problème documenté

- **PROB-001** : Données FIRMS en Near Real-Time avec 0,5 à 6h de décalage → voir [[PROB-001_Donnees_non_temps_reel]]
- **PROB-002** : Couverture nuageuse masquant les feux à certaines périodes → voir [[PROB-002_Couverture_nuageuse]]
- **PROB-003** : Absence de données terrain étiquetées pour Madagascar → voir [[PROB-003_Manque_labels_terrain]]

---

## 3. OBJECTIFS DU PROJET

### 3.1 Objectif général

Créer une **plateforme intelligente hybride** qui transforme des données satellites brutes en alertes et rapports compréhensibles pour lutter contre les feux de brousse et la déforestation à Madagascar.

### 3.2 Objectifs spécifiques

| # | Objectif | Indicateur de succès |
|---|----------|---------------------|
| OS1 | Collecter automatiquement les données FIRMS/Sentinel | Pipeline fonctionnel, données fraîches quotidiennement |
| OS2 | Classifier feu / non-feu avec ML | Accuracy ≥ 85% sur données Madagascar |
| OS3 | Segmenter les zones déforestées avec DL | IoU ≥ 0.70 sur images Sentinel-2 |
| OS4 | Prédire les zones à risque (48–72h) | Précision prédictive mesurable |
| OS5 | Générer des rapports en langage naturel | Rapport lisible sans expertise technique |
| OS6 | Automatiser l'ensemble du pipeline via n8n | Zéro intervention manuelle quotidienne |

---

## 4. PÉRIMÈTRE DU PROJET

### 4.1 Ce que le projet FAIT

- Collecte automatique des données satellites (NASA FIRMS, Sentinel-2)
- Analyse ML/DL des feux et de la déforestation
- Génération d'alertes intelligentes et rapports via IA générative
- Dashboard de visualisation géographique
- Automatisation complète via n8n

### 4.2 Ce que le projet NE FAIT PAS

- ❌ Intervention directe sur le terrain
- ❌ Remplacement des décideurs humains
- ❌ Achat de données payantes
- ❌ Développement d'une application mobile (phase 1)
- ❌ Intégration temps réel strict (NRT = quasi temps réel)

---

## 5. ARCHITECTURE TECHNIQUE (RÉSUMÉ)

```
[APIS SATELLITES] → [PRÉTRAITEMENT PYTHON/QGIS] → [ML/DL]
       ↓                                               ↓
[BASE DE DONNÉES] ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←←
       ↓
[ORCHESTRATION n8n]
       ↓
[IA GÉNÉRATIVE (Ollama / Groq)]
       ↓
[ALERTES / RAPPORTS / DASHBOARD]
```

*Architecture détaillée → voir [[04_Architecture_Globale]]*

---

## 6. STACK TECHNOLOGIQUE

### 6.1 Données & APIs

| Outil | Rôle | Coût |
|-------|------|------|
| NASA FIRMS API | Détection feux NRT (MODIS + VIIRS) | Gratuit |
| NASA Earthdata | Archives MODIS, données climatiques | Gratuit |
| Copernicus Sentinel Hub | Images haute résolution (10m) | Gratuit (quota) |
| Hansen GFC | Déforestation historique | Gratuit |

### 6.2 Traitement & IA

| Outil | Rôle | Coût |
|-------|------|------|
| Python 3.10+ | Langage principal | Gratuit |
| NumPy, Pandas | Manipulation données | Gratuit |
| Rasterio, GeoPandas | Traitement données géospatiales | Gratuit |
| Scikit-learn | ML (Random Forest, SVM, XGBoost) | Gratuit |
| TensorFlow / PyTorch | DL (CNN, U-Net, LSTM) | Gratuit |
| QGIS | Visualisation SIG | Gratuit |

### 6.3 Automatisation & IA Générative

| Outil | Rôle | Coût |
|-------|------|------|
| n8n | Orchestration workflows | Gratuit (self-hosted) |
| Ollama + Llama 3 | IA générative locale | Gratuit |
| Groq API | IA générative rapide (backup) | Gratuit (quota) |
| Hugging Face | Modèles NLP (backup) | Gratuit (quota) |

---

## 7. RESSOURCES DU PROJET

### 7.1 Ressources humaines

| Rôle | Personne | Disponibilité |
|------|----------|---------------|
| Porteur / Développeur IA | Étudiant L3 | Temps plein |
| Expert environnement | Consultatif | Ponctuel |
| Encadrante académique | Mme Larissa | Hebdomadaire |
| Acteurs terrain (validation) | ONG locales | Ponctuel |

### 7.2 Ressources matérielles

| Ressource | Détail |
|-----------|--------|
| PC de développement | Standard (RAM ≥ 8GB recommandé) |
| Connexion Internet | Indispensable pour APIs |
| Google Colab (GPU) | Entraînement DL gratuit |
| GitHub | Versioning du code |

### 7.3 Ressources financières

| Phase | Budget estimé |
|-------|---------------|
| Phase 1 (prototype) | 0 Ar |
| Phase 2 (évolution) | Cloud léger optionnel |
| Phase 3 (déploiement) | Partenariat ONG / bailleurs |

---

## 8. LIVRABLES ATTENDUS

| # | Livrable | Deadline |
|---|----------|----------|
| L1 | Pipeline de collecte automatique fonctionnel | Fin mois 1 |
| L2 | Modèle ML de classification (Random Forest baseline) | Semaine 6 |
| L3 | Modèle DL de segmentation (U-Net) | Semaine 9 |
| L4 | Workflow n8n complet | Semaine 10 |
| L5 | Rapports IA générative | Semaine 11 |
| L6 | Dashboard de visualisation | Semaine 11 |
| L7 | Mémoire L3 rédigé | Semaine 12 |
| L8 | Présentation soutenance | Semaine 12 |

---

## 9. RISQUES IDENTIFIÉS

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Quota API dépassé | Moyenne | Élevé | Multi-sources + cache local |
| Mauvaise qualité données Madagascar | Haute | Élevé | Transfer learning + augmentation |
| PC insuffisant pour DL | Moyenne | Moyen | Google Colab GPU |
| Manque de données terrain | Haute | Élevé | Labels semi-supervisés + PROB-003 |
| Délai NRT (PROB-001) | Certaine | Moyen | Prédiction ML pour anticiper |
| Nuages (PROB-002) | Haute (saison) | Moyen | Multi-capteurs (radar Sentinel-1) |

---

## 10. CRITÈRES DE RÉUSSITE (POUR LE JURY)

1. **Fonctionnel** : Le pipeline collecte, analyse et alerte sans intervention manuelle
2. **Précis** : Les modèles ML/DL atteignent les seuils fixés (OS2, OS3)
3. **Compréhensible** : Les rapports IA sont lisibles par un non-technicien
4. **Documenté** : Le mémoire explique chaque choix technique et scientifique
5. **Réplicable** : Tout le code est open source et reproductible

---

*Références → [[REF-001_NASA_FIRMS_API]] | [[REF-002_AFIS_System]] | [[REF-003_Copernicus_Sentinel]]*
*Architecture → [[04_Architecture_Globale]]*
*Plan de travail → [[03_Plan_Travail_3_Mois]]*
