import random

class MadFireNetService:
    @staticmethod
    def predict_risk(features: dict) -> dict:
        """
        Simule l'inférence du modèle XGBoost (JeryMotroXGB) pour le prototype.
        Dans la version finale, ce service chargera xgb_jerymotrnet_v2.pkl.
        """
        # Simulation d'un calcul de risque basé sur le FRP
        frp = features.get("frp", 0)
        
        if frp > 50:
            risk_score = random.uniform(0.85, 0.99)
            niveau = "CRITIQUE"
        elif frp > 15:
            risk_score = random.uniform(0.60, 0.84)
            niveau = "ÉLEVÉ"
        else:
            risk_score = random.uniform(0.10, 0.59)
            niveau = "MODÉRÉ"

        return {
            "risk_score": round(risk_score, 2),
            "niveau_risque": niveau,
            "model_version": "XGBoost-V2-Prototype"
        }
