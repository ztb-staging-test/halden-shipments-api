import os

os.environ["HALDEN_API_KEYS"] = "tests:k-test-local"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)
AUTH = {"X-API-Key": "k-test-local"}


def test_requires_api_key():
    assert client.get("/shipments").status_code == 422
    assert client.get("/shipments", headers={"X-API-Key": "nope"}).status_code == 401


def test_book_and_track():
    cus = client.post("/customers", json={"name": "Nordhafen GmbH", "email": "ops@nordhafen.example"}, headers=AUTH).json()
    shp = client.post(
        "/shipments",
        json={"customer_id": cus["id"], "origin": "Rotterdam, NL", "destination": "Leipzig, DE", "weight_kg": 820, "carrier": "DHL"},
        headers=AUTH,
    ).json()
    event = {"shipment_id": shp["id"], "status": "delivered", "location": "Leipzig", "occurred_at": "2026-06-02T10:00:00Z"}
    assert client.post("/tracking/events", json=event, headers=AUTH).status_code == 202
    assert client.get(f"/shipments/{shp['id']}", headers=AUTH).json()["status"] == "delivered"
