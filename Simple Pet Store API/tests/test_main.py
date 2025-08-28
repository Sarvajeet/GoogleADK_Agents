from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test__pets():
    response = client.get("/pets")
    assert response.status_code == 200

def test__pets_petId():
    response = client.get("/pets/123")
    assert response.status_code == 200
