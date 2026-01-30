# 🛠 FireProject - Problèmes et Solutions
#FireProject #Problem #Solution #DailyNote #Avancement
[[Glossaire_Tags]]

---
## 📌 Métadonnées
**ID Problème :** PROB-001  
**Date découverte :** 2026-01-29  
**Titre :** Données satellites non en temps réel  
**Source / Remarque :** Commentaire en cours de cours création d’entreprise  
**Priorité :** Haute 🔴  
**Impact :** Risque de retard d’alerte, catastrophe destructrice  

---
## 🔴 Description du problème
Les données satellites FIRMS (MODIS/VIIRS) sont publiées en Near Real-Time (NRT) mais avec un **décalage de 0,5 à 6 heures** selon le capteur et la zone.  
En cas de feux de brousse massif, ce retard pourrait **diminuer la réactivité et augmenter l’impact destructeur**.

---
## ✅ Solutions proposées
1. **Prédiction ML/DL** : Random Forest, XGBoost, CNN/LSTM pour séries temporelles d’images. Anticiper zones à risque.  
2. **Multi-source / Multi-capteurs** : Combiner MODIS + VIIRS + Sentinel-2 pour fiabilité et rapidité.  
3. **Workflow automatisé (n8n/API)** : Pipeline automatique pour récupérer données dès publication et générer alertes immédiates.  
4. **Système de priorité des alertes** : Classer alertes selon intensité, zone et densité végétation.  

---
## 📝 Notes supplémentaires
- L’outil est un support d’alerte, pas une solution de gestion directe.  
- ML/DL minimise le retard et anticipe les incendies.  

---
## 📅 Historique & Avancement
| Date       | Action / Avancement       | Tag                 |
| ---------- | ------------------------- | ------------------- |
| 2026-01-29 | Problème identifié        | #Problem #DailyNote |
