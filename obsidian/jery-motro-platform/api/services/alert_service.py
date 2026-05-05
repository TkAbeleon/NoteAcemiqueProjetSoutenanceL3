class AlertService:
    @staticmethod
    def send_alert(risk_score: float, region: str):
        """
        Logique de déclenchement selon la matrice V3.
        """
        img_urls = ["https://i.ibb.co/thermique_mock.png"]
        
        if risk_score > 0.80:
            img_urls.append("https://i.ibb.co/visible_mock.png")
            return {"status": "sent", "level": "ALERTE HAUTE", "channels": ["Email", "WhatsApp", "SMS"], "images": img_urls}
        elif risk_score > 0.60:
            img_urls.append("https://i.ibb.co/visible_mock.png")
            return {"status": "sent", "level": "ALERTE MOYENNE", "channels": ["Email", "WhatsApp"], "images": img_urls}
        elif risk_score > 0.40:
            return {"status": "sent", "level": "ALERTE BASSE", "channels": ["Email"], "images": img_urls}
        
        return {"status": "ignored", "level": "AUCUN RISQUE"}
