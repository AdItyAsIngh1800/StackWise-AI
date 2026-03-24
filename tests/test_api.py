from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_recommend():
    response = client.post("/recommend", json={
        "project_type": "api",
        "team_languages": ["python"],
        "low_ops": True,
        "expected_scale": "medium"
    })
    assert response.status_code == 200

def test_natural_language():
    response = client.post("/recommend/natural-language", json={
        "query": "scalable backend with low ops"
    })
    assert response.status_code == 200