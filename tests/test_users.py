from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_user_by_id_returns_public_profile():
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "email": "ada@example.com", "name": "Ada Lovelace"}


def test_get_user_by_id_returns_404_for_missing_user():
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
