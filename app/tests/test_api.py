from fastapi.testclient import TestClient

from payment_api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness_endpoint():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_payment():
    response = client.post(
        "/payments",
        json={
            "amount": 150.50,
            "currency": "EGP",
            "description": "Test payment",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["amount"] == 150.50
    assert data["currency"] == "EGP"
    assert data["status"] == "simulated"
    assert "payment_id" in data


def test_reject_invalid_payment():
    response = client.post(
        "/payments",
        json={
            "amount": -10,
            "currency": "EGP",
            "description": "Invalid payment",
        },
    )

    assert response.status_code == 422


def test_payment_not_found():
    response = client.get("/payments/does-not-exist")

    assert response.status_code == 404
