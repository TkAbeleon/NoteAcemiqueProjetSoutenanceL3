import os
import requests

class RAGService:
    @staticmethod
    def generate_response(question: str) -> dict:
        """
        Simule le RAG (Retrieval-Augmented Generation) avec ChromaDB et Groq.
        Dans le futur, cela interrogera d'abord ChromaDB pour le contexte.
        """
        # Mock du contexte récupéré depuis ChromaDB
        mock_context = "2026-03-30 : 52 détections VIIRS. FRP max 187MW (Menabe). Cluster 3 à risque."
        
        system_prompt = """Tu es JeryMotro AI, assistant spécialisé de la plateforme JeryMotro Platform (Madagascar).
RÈGLES ABSOLUES :
1. Tu réponds UNIQUEMENT sur les données du projet.
2. Si la question dépasse les données disponibles → réponds EXACTEMENT : 'Je suis limité aux données JeryMotro. Consultez les sources NASA directement.'"""

        groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Pour le prototype sans clé API, on renvoie une réponse simulée intelligente
        if not groq_api_key:
            if "détections" in question.lower() or "aujourd'hui" in question.lower():
                return {"response": "52 détections VIIRS ce 30/03/2026, FRP max 187MW (Menabe).", "sources": ["ChromaDB: Résumé Journalier"]}
            elif "risque" in question.lower():
                return {"response": "Menabe, cluster 3 : risque=0.89, FRP=187MW.", "sources": ["ChromaDB: Clusters Actifs"]}
            else:
                return {"response": "Je suis limité aux données JeryMotro. Consultez les sources NASA directement.", "sources": []}
        
        # Intégration réelle Groq (llama3-8b-8192)
        headers = {"Authorization": f"Bearer {groq_api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": system_prompt + f"\n\nCONTEXTE: {mock_context}"},
                {"role": "user", "content": question}
            ]
        }
        
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
            data = res.json()
            return {
                "response": data["choices"][0]["message"]["content"],
                "sources": ["ChromaDB (Mock)"]
            }
        except Exception as e:
            return {"response": f"Erreur API Groq : {str(e)}", "sources": []}
