from starlette.testclient import TestClient


def test_health_check_endpoint(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "HealthGuide AI" in data["service"]
    assert "supported_languages" in data
    assert "en" in data["supported_languages"]
    assert "ta" in data["supported_languages"]
