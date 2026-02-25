# 📚 REF-003 — Copernicus Sentinel Hub (ESA)
#FireProject #Reference #API #Sentinel2 #Documentation
[[Glossaire_Tags]] | [[05_APIs_et_Donnees]] | [[00_INDEX]]

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Titre** | ESA Copernicus Data Space Ecosystem |
| **Source** | ESA (Agence Spatiale Européenne) |
| **Lien** | https://dataspace.copernicus.eu |
| **API** | https://shapps.dataspace.copernicus.eu |
| **Accès** | Compte gratuit — pas de carte bancaire |

---

## Produits disponibles

| Produit | Usage |
|---------|-------|
| Sentinel-2 L2A | Images optiques corrigées atmosphériquement |
| Sentinel-1 GRD | Radar SAR tout temps |
| Sentinel-3 OLCI | Grands incendies (1km résolution) |

---

## Accès Python recommandé

```bash
pip install sentinelhub
pip install odc-stac  # Alternative via STAC API
```

---

## Notes

- Quota gratuit : ~25GB/mois de téléchargement
- Alternative : Google Earth Engine (accès académique gratuit)
- Sentinel-1 → solution pour [[PROB-002_Couverture_nuageuse]]

---

## Dataset lié

- [[08_Dataset_Sentinel2]]
