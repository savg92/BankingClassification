from fastapi.testclient import TestClient

from apps.backend.app.main import app, service


class StubProvider:
    async def embed(self, text: str) -> list[float]:
        return [0.1] * 768


def test_health_and_analyze_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(service, "provider", StubProvider())

    client = TestClient(app)
    health_response = client.get("/health")
    assert health_response.status_code == 200

    analyze_response = client.post("/analyze", json={"text": "Please review this transfer"})
    assert analyze_response.status_code == 200

    payload = analyze_response.json()
    assert "embedding" in payload
    assert "intent" in payload
    assert "sentiment" in payload
    assert len(payload["embedding"]) == 768
