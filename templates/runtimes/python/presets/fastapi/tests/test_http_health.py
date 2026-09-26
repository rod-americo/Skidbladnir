
from fastapi.testclient import TestClient

from {{PROJECT_SLUG}}.interfaces.http.app import create_app


def test_health_route() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
