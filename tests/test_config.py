from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_config_returns_read_only_service_metadata():
    response = client.get("/config")

    assert response.status_code == 200
    assert response.json() == {
        "service": "pr-review-sandbox",
        "environment": "sandbox",
        "features": ["users", "payments", "audit_log"],
    }


def test_get_config_can_omit_features():
    response = client.get("/config?include_features=false")

    assert response.status_code == 200
    assert response.json() == {
        "service": "pr-review-sandbox",
        "environment": "sandbox",
    }


def test_get_config_accepts_explicit_feature_inclusion():
    response = client.get("/config?include_features=true")

    assert response.status_code == 200
    assert response.json()["features"] == ["users", "payments", "audit_log"]
