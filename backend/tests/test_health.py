from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "saathi-api"


def test_conversation_routes_scheme():
    response = client.post("/api/v1/conversation", json={"message": "scholarship ke liye kya chahiye?"})
    assert response.status_code == 200
    assert response.json()["intent"] == "scheme"


def test_conversation_rejects_empty_message():
    response = client.post("/api/v1/conversation", json={"message": ""})
    assert response.status_code == 422
