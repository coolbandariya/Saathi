from fastapi.testclient import TestClient

from app.main import app


def test_outbound_call_requires_explicit_consent():
    response = TestClient(app).post(
        "/api/v1/calls",
        json={"to": "+919999999999", "callback_url": "https://example.test/callback", "consent": False},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "explicit_outbound_call_consent_required"


def test_demo_outbound_call_never_calls_real_provider():
    response = TestClient(app).post(
        "/api/v1/calls",
        json={"to": "+919999999999", "callback_url": "https://example.test/callback", "consent": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "demo"
    assert body["call_id"] == "demo-call-accepted"
