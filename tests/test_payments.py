from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_charge_creates_paid_payment():
    response = client.post(
        "/payments/charge",
        json={"user_id": 1, "amount_cents": 2500, "currency": "USD"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"].startswith("pay_")
    assert body["status"] == "charged"
    assert body["amount_cents"] == 2500
    assert body["currency"] == "USD"


def test_charge_rejects_unknown_user():
    response = client.post(
        "/payments/charge",
        json={"user_id": 999, "amount_cents": 2500, "currency": "USD"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}


def test_charge_rejects_non_positive_amount():
    response = client.post(
        "/payments/charge",
        json={"user_id": 1, "amount_cents": 0, "currency": "USD"},
    )

    assert response.status_code == 422


def test_refund_marks_payment_refunded():
    charge = client.post(
        "/payments/charge",
        json={"user_id": 1, "amount_cents": 4300, "currency": "USD"},
    ).json()

    response = client.post("/payments/refund", json={"payment_id": charge["id"]})

    assert response.status_code == 200
    assert response.json()["status"] == "refunded"


def test_refund_rejects_unknown_payment():
    response = client.post("/payments/refund", json={"payment_id": "pay_missing"})

    assert response.status_code == 404
    assert response.json() == {"detail": "payment not found"}
