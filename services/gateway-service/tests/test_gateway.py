from fastapi.testclient import TestClient
from app.main import app


def test_health():
 client = TestClient(app)
 r = client.get("/api/health")
 assert r.status_code == 200