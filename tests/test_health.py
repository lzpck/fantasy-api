import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """
    Testa se o endpoint /health retorna status 200 e resposta correta.
    """
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}