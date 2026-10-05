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


def test_conversation_marks_human_escalation():
    response = client.post("/api/v1/conversation", json={"message": "मुझे किसी इंसान से बात करनी है"})
    assert response.status_code == 200
    body = response.json()
    assert body["escalated"] is True
    assert body["escalation_reason"] == "explicit_human_request"

def test_agent_returns_provenance_and_confidence():
    response = client.post("/api/v1/agent", json={"message": "सोनीपत मंडी में गेहूं का भाव", "language": "hi"})
    assert response.status_code == 200
    body = response.json()
    assert body["source"]["name"] == "Saathi Demo Mandi"
    assert body["demo"] is True
    assert body["confidence"] is not None

def test_readiness_exposes_provider_state():
    response = client.get("/health/ready")
    assert response.status_code == 200
    body = response.json()
    assert "provider_contracts" in body
    assert "telephony" in body["provider_contracts"]
