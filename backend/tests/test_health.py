from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "Doctor approval" in response.json()["safety_notice"]


def test_intended_use_has_safety_limitation() -> None:
    response = client.get("/api/v1/intended-use")

    assert response.status_code == 200
    assert "does not independently diagnose" in response.json()["limitation"]

