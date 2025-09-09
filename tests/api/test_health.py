from fastapi.testclient import TestClient

from src.main import app


def test_health_ok():
    client = TestClient(app)
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body == {"status": "ok"}
