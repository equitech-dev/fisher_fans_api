import pytest
from .conftest import client

def test_login_success(client, test_user_data):
    # Créer l'utilisateur
    client.post("/v1/users", json=test_user_data)
    
    response = client.post("/v1/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post("/v1/login", data={
        "username": "wrong@email.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_missing_fields(client):
    response = client.post("/v1/login", data={})
    assert response.status_code == 422
