# 🎤 Pitch — JERY MOTRO
**Soutenance L2 — Génie Logiciel**
*RANDRIAMANANTEÑA Tsiky Ny Antsa*

---

## SLIDE 1 — Accroche (30 sec)

Chaque minute, une forêt brûle à Madagascar.
Pourtant, les satellites de la NASA survolent l'île en ce moment même —
et personne n'alerte les communautés concernées.

**JERY MOTRO**, c'est la réponse : quand l'IA donne le pouvoir
au peuple de protéger sa propre forêt.

---

## SLIDE 2 — Plan (15 sec)

Je vais vous présenter en six parties :
le contexte, la problématique, nos objectifs,
notre méthodologie, les résultats attendus,
et nos perspectives.

---

## SLIDE 3 — Contexte (45 sec)

Madagascar est en danger.
Le **2 novembre 2025**, en seulement 24 heures :
**4 384 feux** détectés — soit **1 feu par minute**.

Les données satellites existent, elles sont **gratuites**.
NASA et ESA les publient chaque jour.

Le problème n'est pas le manque d'information.
C'est que **personne ne les transforme en alertes
accessibles aux citoyens malgaches**.

---

## SLIDE 4 & 5 — Problématique (1 min)

Les solutions qui existent aujourd'hui ont trois limites majeures :

- Les outils **mondiaux** ne sont pas adaptés à Madagascar
- Le **géo-portail gouvernemental** existe — mais son accès
  est réservé aux autorités, sur demande
- **Aucun mécanisme d'alerte automatique** ne touche
  les villages, les ONG, les citoyens

Le paradoxe est brutal :
Le **24 septembre 2025**, un feu de **1 389 MW** a été détecté —
l'équivalent d'une centrale électrique.

Résultat ?
- Villages alertés : **aucun**
- ONG locales informées : **sur autorisation**
- Citoyens prévenus : **zéro**

---

## SLIDE 6 — Question de recherche (20 sec)

Ce constat nous amène à notre question centrale :

> *Comment développer une plateforme logicielle complète —
> collecte, apprentissage automatique, API, interface et alertes —
> qui améliore la détection des feux de brousse à Madagascar
> en exploitant exclusivement les données FIRMS ?*

---

## SLIDE 7 & 8 — Objectifs (45 sec)

JERY MOTRO a cinq objectifs concrets :

1. **Collecter** automatiquement les données satellites
   chaque jour, sans intervention manuelle
2. **Analyser** par IA — détecter les feux,
   mesurer la déforestation
3. **Alerter** en temps utile — score de risque
   avant que le feu ne s'étende
4. **Produire** des rapports lisibles en **malgache et français**
5. **Visualiser** sur un dashboard interactif pour Madagascar

Le tout orchestré automatiquement par n8n,
de la source satellite jusqu'à l'alerte SMS.

---

## SLIDE 9 — Architecture en 7 couches (1 min)

Notre architecture suit une chaîne causale en 7 couches :

| Couche | Rôle |
|--------|------|
| 1. Sources | NASA FIRMS · Sentinel-2 · Hansen GFC |
| 2. Collecte | n8n déclenche les téléchargements à 06h00 |
| 3. Prétraitement | Calcul NDVI, NBR — Python |
| 4. Analyse IA | Machine Learning + Deep Learning |
| 5. Base de données | Historique, scores de risque |
| 6. IA générative | Rapports automatiques — Llama 3 |
| 7. Sorties | Carte · Email · SMS · PDF |

Chaque couche alimente la suivante.
Aucune intervention humaine n'est nécessaire.

---

## SLIDE 10 & 14 — Résultats attendus (1 min)

La plateforme produit **six livrables concrets** :

- 📋 **Rapport quotidien** — chaque matin, résumé des feux de la veille
- ⚡ **Alertes automatiques** — email et SMS si risque > 70%
- 🗺️ **Carte interactive** — tous les feux actifs sur Madagascar
- 📈 **Prédiction 48–72 h** — zones susceptibles de brûler
- 🌲 **Suivi déforestation** — comparaison annuelle U-Net
- 📄 **Rapport PDF hebdomadaire** — synthèse pour décideurs

**Exemple concret :**
Le 12 mars 2026, le système génère automatiquement :
> *"47 feux détectés. Menabe : 23 foyers, intensité très élevée.
> Recommandation : mobiliser les équipes dans les 48h."*

Niveau d'alerte : **ÉLEVÉ** — sans qu'un seul humain
n'ait appuyé sur un bouton.

---

## SLIDE 15 & 16 — Notre différence (45 sec)

Ce qui distingue JERY MOTRO des systèmes existants :

| Système actuel | JERY MOTRO |
|----------------|------------|
| Accès réservé | ✅ Gratuit pour tous |
| Français uniquement | ✅ Malgache + Français |
| Code propriétaire | ✅ Open-source GitHub |
| Pour le gouvernement | ✅ Pour les communautés |

Et notre **triple innovation IA** :

1. **Machine Learning** — prédit les zones à risque
   sur 76 000 feux historiques
2. **Deep Learning** — détecte la fumée en quasi temps réel
   avant que le feu ne s'étende
3. **IA Générative** — *le game changer* —
   transforme des alertes techniques en messages
   compréhensibles pour les populations locales

---

## SLIDE 17 — Conclusion (30 sec)

JERY MOTRO démontre trois choses fondamentales :

- Les données satellites gratuites → **exploitation intelligente possible**
- L'alerte automatique → **réaction plus efficace**
- L'IA accessible → **décisions locales plus rapides**

Et demain :
- Application mobile pour les communautés rurales
- Intégration données météo
- Partenariat ONG et Ministère de l'Environnement
- Extension à d'autres pays africains

**Détecter aujourd'hui pour protéger demain.**

---

## SLIDE 18 — Clôture (10 sec)

Merci pour votre attention.
Je suis disponible pour répondre à vos questions.

---

## ⏱️ Minutage total : ~8 min 30

| Section | Durée |
|---------|-------|
| Accroche | 30 s |
| Plan | 15 s |
| Contexte | 45 s |
| Problématique | 1 min |
| Question | 20 s |
| Objectifs | 45 s |
| Architecture | 1 min |
| Résultats | 1 min |
| Différence | 45 s |
| Conclusion | 30 s |
| Clôture | 10 s |
| **TOTAL** | **~7 min 10 s** |

> 💡 **Conseil** : Laissez ~1 min 50 s de marge
> pour les transitions et les respirations.
> Chronométrez au moins 2 fois avant la soutenance.