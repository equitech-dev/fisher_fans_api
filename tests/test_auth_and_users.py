import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.enum import StatusEnum

client = TestClient(app)

# Données de test partagées
TEST_USER_DATA = {
    "name": "Doe",
    "firstname": "John",
    "email": "john.doe@example.com",
    "password": "password123",
    "phone": "1234567890",
    "status": StatusEnum.INDIVIDUAL.value  # Utiliser INDIVIDUAL au lieu de PARTICULIER
}

TEST_USER_LOGIN = {
    "username": "john.doe@example.com",
    "password": "password123"
}

class TestAuth:
    def test_login_success(self):
        # Créer d'abord l'utilisateur
        client.post("/v1/users", json=TEST_USER_DATA)
        
        # Tenter de se connecter
        response = client.post("/v1/login", data=TEST_USER_LOGIN)
        assert response.status_code == 200
        assert "token" in response.json()

    def test_login_invalid_credentials(self):
        response = client.post("/v1/login", data={
            "username": TEST_USER_LOGIN["username"],
            "password": "wrongpassword"
        })
        assert response.status_code == 401

class TestUsers:
    def test_create_user_success(self):
        response = client.post("/v1/users", json={
            **TEST_USER_DATA,
            "email": "new.user@example.com"  # email différent pour éviter le conflit
        })
        assert response.status_code == 201
        assert "token" in response.json()

    def test_create_user_duplicate_email(self):
        # Tenter de créer un utilisateur avec le même email
        response = client.post("/v1/users", json=TEST_USER_DATA)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_get_user_profile(self):
        # Se connecter d'abord pour obtenir le token
        login_response = client.post("/v1/login", data=TEST_USER_LOGIN)
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Obtenir le profil utilisateur
        response = client.get("/v1/users/1", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == TEST_USER_DATA["email"]

    def test_get_user_full_profile(self):
        # Se connecter d'abord pour obtenir le token
        login_response = client.post("/v1/login", data=TEST_USER_LOGIN)
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Obtenir le profil complet
        response = client.get("/v1/users/1/profile", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "boats" in data
        assert "trips" in data
        assert "reservations" in data
        assert "logs" in data

    def test_update_user(self):
        # Se connecter d'abord pour obtenir le token
        login_response = client.post("/v1/login", data=TEST_USER_LOGIN)
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Mettre à jour l'utilisateur
        update_data = {"phone": "0987654321"}
        response = client.put("/v1/users/1", headers=headers, json=update_data)
        assert response.status_code == 200
        assert response.json()["phone"] == update_data["phone"]

    def test_delete_user_unauthorized(self):
        # Se connecter en tant qu'utilisateur normal
        login_response = client.post("/v1/login", data=TEST_USER_LOGIN)
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Tenter de supprimer un utilisateur
        response = client.delete("/v1/users/1", headers=headers)
        assert response.status_code == 403

    def test_access_without_token(self):
        response = client.get("/v1/users/1")
        assert response.status_code == 401

    def test_invalid_token(self):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/v1/users/1", headers=headers)
        assert response.status_code == 401

    @pytest.mark.parametrize("missing_field", ["email", "password", "status"])
    def test_create_user_missing_required_fields(self, missing_field):
        data = TEST_USER_DATA.copy()
        del data[missing_field]
        response = client.post("/v1/users", json=data)
        assert response.status_code == 422
