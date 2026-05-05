from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Vérifie que l'API est en ligne."""
    response = client.get("/api/health")
    assert response.status_code == 200, "Le endpoint /api/health doit retourner 200"
    data = response.json()
    assert data["status"] == "ok"
    assert "JeryMotro" in data["system"]
    print("✅ Test /api/health : OK")

def test_get_detections():
    """Vérifie que la route des détections renvoie bien les données depuis Supabase."""
    # On limite à 5 pour ne pas surcharger la base pendant le test
    response = client.get("/api/detections/?limit=5")
    assert response.status_code == 200, f"Erreur {response.status_code}: {response.text}"
    
    data = response.json()
    assert isinstance(data, list), "La réponse doit être une liste"
    
    print(f"✅ Test /api/detections : OK ({len(data)} détections récupérées depuis Supabase)")
    
    if len(data) > 0:
        premier_feu = data[0]
        print(f"   🔥 Exemple de donnée : Source={premier_feu.get('source')}, FRP={premier_feu.get('frp')}, Risque={premier_feu.get('niveau_risque')}")

def test_get_clusters():
    """Vérifie la route des clusters."""
    response = client.get("/api/clusters/?limit=5")
    assert response.status_code == 200, f"Erreur {response.status_code}: {response.text}"
    print(f"✅ Test /api/clusters : OK ({len(response.json())} clusters récupérés)")

def test_get_alerts():
    """Vérifie la route des alertes."""
    response = client.get("/api/alerts/?limit=5")
    assert response.status_code == 200, f"Erreur {response.status_code}: {response.text}"
    print(f"✅ Test /api/alerts : OK ({len(response.json())} alertes récupérées)")

if __name__ == "__main__":
    print("🚀 Lancement des tests du Backend JeryMotro...")
    try:
        test_health_check()
        test_get_detections()
        test_get_clusters()
        test_get_alerts()
        print("\n🎉 TOUS LES TESTS SONT AU VERT ! Le backend fonctionne parfaitement avec la BDD.")
    except AssertionError as e:
        print("\n❌ ÉCHEC DU TEST :", e)
    except Exception as e:
        print("\n❌ ERREUR INATTENDUE :", e)
        print("💡 Astuce: Vérifiez que vous avez bien fait 'pip install -r requirements.txt httpx'")
