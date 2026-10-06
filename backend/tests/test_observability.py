from fastapi.testclient import TestClient
from app.main import app


def test_correlation_id_is_returned_and_echoed() -> None:
    client = TestClient(app)
    correlation_id = "hackathon-demo-123"
    response = client.post(
        "/api/v1/conversation",
        headers={"X-Correlation-ID": correlation_id},
        json={"message": "नमस्ते", "language": "hi"},
    )
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == correlation_id
    assert response.json()["correlation_id"] == correlation_id


def test_correlation_id_is_generated_when_missing() -> None:
    response = TestClient(app).post(
        "/api/v1/conversation",
        json={"message": "नमस्ते", "language": "hi"},
    )
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"]
    assert response.json()["correlation_id"] == response.headers["X-Correlation-ID"]


def test_health_metrics_endpoint_is_safe_and_structured() -> None:
    response = TestClient(app).get("/health/metrics")
    assert response.status_code == 200
    body = response.json()
    assert "requests" in body
    assert "latency_ms" in body
