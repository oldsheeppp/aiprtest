from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_service_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "pr-review-sandbox",
        "status": "ok",
        "version": "0.1.0",
    }


def test_readiness_reports_in_memory_store_counts():
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["ready"] is True
    assert response.json()["checks"]["users"] >= 2
    assert "audit_events" in response.json()["checks"]
