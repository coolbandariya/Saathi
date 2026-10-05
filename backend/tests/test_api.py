from fastapi.testclient import TestClient
from app.main import app

def test_agent_endpoint_returns_provenance():
    client=TestClient(app)
    response=client.post('/api/v1/agent',json={'message':'गेहूं का मंडी भाव क्या है?','language':'hi'})
    assert response.status_code == 200
    data=response.json()
    assert data['intent']=='farming'
    assert data['source']['name']=='Saathi Demo Mandi'
    assert data['demo'] is True

def test_liveness():
    assert TestClient(app).get('/health/live').json()['status']=='alive'
