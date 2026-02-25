# 🧠 JeryMotro AI — RAG + Groq
#JeryMotro #MemoireL3 #API #RAG #DecisionSupport
[[Glossaire_Tags]] | [[00_INDEX]] | [[09_FastAPI_Backend]]

---

## 1. PRINCIPE

> JeryMotro AI répond **uniquement** aux questions sur les données du projet.
> Elle n'est pas un LLM généraliste — c'est un expert des données JeryMotro.

**Flux :**
```
Question utilisateur
    → ChromaDB : trouver contexte pertinent (top 5 documents)
    → Groq API : LLM avec contexte + contrainte
    → Réponse précise, citant les données réelles
```

---

## 2. STRUCTURE ChromaDB

```python
# Ce qui est stocké dans ChromaDB après chaque run pipeline

chroma_docs = [
    # Résumé journalier
    "2026-02-23 : 47 détections. FRP max 234MW (Menabe). 3 clusters actifs. Risque élevé S-O.",

    # Métriques JeryMotroNet
    "JeryMotroNet XGBoost : Recall=0.87, Précision=0.81, AUC=0.91. +31% recall vs NASA brut.",

    # Clusters actifs
    "Cluster 5 (2026-02-23) : 12 points, FRP total 847MW, centre -20.3/44.1, risque=0.92",

    # Tendances hebdomadaires
    "Semaine 08/2026 : 312 feux, +18% vs semaine précédente. Regions: Menabe(34%), Boeny(21%)",
]
```

---

## 3. SYSTEM PROMPT

```python
SYSTEM_PROMPT = """
Tu es JeryMotro AI, assistant spécialisé de la plateforme JeryMotro Platform (Madagascar).

RÈGLES ABSOLUES :
1. Tu réponds UNIQUEMENT sur les données du projet (détections FIRMS, clusters HDBSCAN,
   prédictions JeryMotroNet, métriques, historique Madagascar).
2. Si la question dépasse les données disponibles, réponds EXACTEMENT :
   "Je suis limité aux données JeryMotro. Consultez les sources NASA directement."
3. Cite toujours les données concrètes (dates, FRP, régions, scores).
4. Réponds en français. Sois précis et concis (max 200 mots).
5. Ne génère JAMAIS d'informations non présentes dans le contexte fourni.
"""
```

---

## 4. Modèles Groq disponibles

| Modèle | Vitesse | Qualité | Usage recommandé |
|--------|---------|---------|-----------------|
| `llama3-8b-8192` | ⚡ Très rapide | Bonne | Requêtes simples (stats, chiffres) |
| `llama3-70b-8192` | 🐢 Lent | Excellente | Analyses complexes |
| `mixtral-8x7b-32768` | Moyen | Très bonne | Requêtes longues contexte |

→ **Par défaut :** `llama3-8b-8192` (quota généreux, rapide)

---

*FastAPI endpoint /chat → [[09_FastAPI_Backend]]*
