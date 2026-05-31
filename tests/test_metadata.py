from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_metadata_returns_read_only_capabilities():
    response = client.get("/metadata")

    assert response.status_code == 200
    assert response.json() == {
        "service": "pr-review-sandbox",
        "environment": "sandbox",
        "capabilities": ["users", "payments", "audit_log"],
    }
