# 🖥️ Frontend — Décision React vs Flutter
#JeryMotro #MemoireL3 #Frontend #Decision
[[Glossaire_Tags]] | [[00_INDEX]] | [[01_Cahier_des_Charges]]

---

> ⚠️ **DÉCISION OBLIGATOIRE avant la fin de S1 (01/03/2026)**
> Inscrire la décision finale dans la section 4 de ce document.

---

## 1. ANALYSE COMPARATIVE

### 1.1 React (JavaScript / TypeScript)

**Stack :** React 18 + TypeScript + Leaflet.js + Recharts + Tailwind CSS

```
✅ Pour le projet JeryMotro :
- Leaflet.js → cartes interactives très matures (affichage points feux)
- Recharts → graphiques saisonniers élégants
- Fetch API / Axios → consommation FastAPI simple
- Déploiement gratuit : Vercel / Netlify
- Docker : image node:20-alpine, build optimisé

⚠️ Points de vigilance :
- JS/TS à maîtriser si pas encore acquis
- Gestion état : Context API (simple) ou Zustand (léger)
```

**Architecture React recommandée pour JeryMotro :**
```
src/
├── components/
│   ├── MapView.jsx          ← Leaflet + marqueurs feux (couleur = risque)
│   ├── RiskMap.jsx          ← Heatmap grille ConvLSTM J+1
│   ├── Dashboard.jsx        ← Graphiques Recharts (saisonniers, MODIS vs VIIRS)
│   ├── ChatPanel.jsx        ← Interface JeryMotro AI
│   ├── AlertPanel.jsx       ← Historique alertes temps réel
│   └── StatsBar.jsx         ← Métriques du jour (nb feux, FRP max, etc.)
├── services/
│   └── api.js               ← Tous les appels FastAPI (axios instance)
├── hooks/
│   ├── useDetections.js     ← Hook personnalisé → GET /detections
│   └── useRiskMap.js        ← Hook → GET /risk-map
├── App.jsx
└── index.js
```

**Code exemple — MapView.jsx :**
```jsx
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import { useDetections } from '../hooks/useDetections';

export default function MapView() {
  const { detections, loading } = useDetections({ min_frp: 5 });

  // Couleur selon risk_score
  const getRiskColor = (score) => {
    if (score > 0.8) return '#d32f2f';   // Rouge — critique
    if (score > 0.5) return '#ff9800';   // Orange — élevé
    return '#ffeb3b';                     // Jaune — modéré
  };

  return (
    <MapContainer center={[-18.7, 46.8]} zoom={6} style={{ height: '600px' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {detections.map(d => (
        <CircleMarker
          key={d.id}
          center={[d.latitude, d.longitude]}
          radius={Math.max(3, d.frp / 20)}
          color={getRiskColor(d.risk_score)}
          fillOpacity={0.7}
        >
          <Popup>
            <b>FRP :</b> {d.frp} MW<br/>
            <b>Risque :</b> {(d.risk_score * 100).toFixed(0)}%<br/>
            <b>Capteur :</b> {d.satellite}<br/>
            <b>Date :</b> {d.acq_date}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
```

---

### 1.2 Flutter (Dart)

**Stack :** Flutter 3.x + flutter_map + fl_chart + http package

```
✅ Pour le projet JeryMotro :
- flutter_map → cartes (fonctionnel mais moins riche que Leaflet)
- fl_chart → graphiques acceptables
- Dart : langage propre, typé
- Flutter Web : fonctionne pour déploiement web
- Bonus futur : même codebase → iOS + Android après L3

⚠️ Points de vigilance :
- Dart à apprendre si inconnu
- Flutter Web moins optimisé que React pour dashboards complexes
- Cartes moins matures : flutter_map 4.x (sufficient mais limité)
- Taille bundle web plus lourde
- Moins d'exemples dashboards géospatiaux que React
```

---

## 2. TABLEAU DE DÉCISION

| Critère | Poids | React | Flutter |
|---------|-------|-------|---------|
| Maturité cartes (Leaflet) | 25% | ✅ 5/5 | 🟡 3/5 |
| Facilité dashboard data | 20% | ✅ 5/5 | 🟡 3/5 |
| Déploiement web gratuit | 15% | ✅ 5/5 | 🟡 4/5 |
| Temps d'apprentissage | 15% | 🟡 3/5 | 🟡 3/5 |
| Écosystème / exemples | 10% | ✅ 5/5 | 🟡 3/5 |
| Futur (mobile post-L3) | 10% | 🟡 3/5 | ✅ 5/5 |
| Performance web | 5% | ✅ 5/5 | 🟡 3/5 |
| **Score total** | | **4.35/5** | **3.35/5** |

---

## 3. RECOMMANDATION

> **React est recommandé pour JeryMotro Platform.**

**Raisons principales :**
1. Leaflet.js est la bibliothèque de référence pour les cartes de données géospatiales web
2. L'affichage de 10 000+ points feux avec heatmap risque est plus fluide en React
3. Recharts rend les graphiques saisonniers propres et animés
4. Déploiement Vercel en 5 minutes
5. Plus d'exemples de dashboards environnementaux disponibles

Flutter reste pertinent **si tu prévois de développer une app mobile après la soutenance**.

---

## 4. DÉCISION FINALE

> **⬜ À remplir avant le 01/03/2026**

| Champ | Valeur |
|-------|--------|
| **Choix** | ⬜ React OU ⬜ Flutter |
| **Date de décision** | |
| **Justification** | |
| **Version** | React 18 + TS OU Flutter 3.x |

---

## 5. SETUP INITIAL (selon choix)

### Si React :

```bash
# Dans le dossier frontend/
npx create-react-app . --template typescript
npm install leaflet react-leaflet recharts axios tailwindcss
npm install -D @types/leaflet
```

### Si Flutter Web :

```bash
flutter create madfire_frontend
cd madfire_frontend
flutter config --enable-web

# Dépendances dans pubspec.yaml :
# flutter_map: ^6.0.0
# fl_chart: ^0.67.0
# http: ^1.2.0
# provider: ^6.1.2
```

---

*Cahier des charges → [[01_Cahier_des_Charges]]*
*Docker → [[08_Docker_Infrastructure]]*
*FastAPI → [[09_FastAPI_Backend]]*
