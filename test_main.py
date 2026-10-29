from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Bug Tracker API"}

def test_create_bug():
    response = client.post("/bugs", json={"title": "Test Bug", "description": "This is a test bug"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Bug"
    assert data["id"] == 1
    assert data["status"] == "open"

def test_get_bugs():
    response = client.get("/bugs")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_bug_by_id():
    response = client.get("/bugs/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Bug"

def test_delete_bug():
    response = client.delete("/bugs/1")
    assert response.status_code == 200
    response = client.get("/bugs/1")
    assert response.status_code == 404
