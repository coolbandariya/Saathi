from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_and_ready():
    assert client.get("/health").status_code == 200
    assert client.get("/ready").json()["ready"] is True

def test_conversation_contract():
    response = client.post("/api/v1/conversation", json={"message":"mandi ka bhav batao","language":"hi"})
    assert response.status_code == 200
    body=response.json()
    assert body["intent"] == "farming"
    assert body["request_id"]

def test_empty_message_is_rejected():
    assert client.post("/api/v1/conversation", json={"message":""}).status_code == 422
