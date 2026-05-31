from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_admin_audit_log_requires_admin_role():
    response = client.get("/admin/audit-log", headers={"X-Role": "user"})

    assert response.status_code == 403
    assert response.json() == {"detail": "admin role required"}


def test_admin_audit_log_accepts_admin_role():
    response = client.get("/admin/audit-log", headers={"X-Role": "admin"})

    assert response.status_code == 200
    assert response.json()["events"]
