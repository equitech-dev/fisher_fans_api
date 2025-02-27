import pytest
from fastapi.testclient import TestClient
from app.main import app

class TestBase:
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient, auth_headers):
        """
        Setup de base pour tous les tests qui héritent de cette classe.
        Initialise le client et les headers d'authentification.
        """
        self.client = client
        self.headers = auth_headers

    def create_test_resource(self, endpoint: str, data: dict):
        """
        Méthode utilitaire pour créer une ressource de test
        """
        response = self.client.post(endpoint, json=data, headers=self.headers)
        assert response.status_code in [200, 201]
        return response.json()

    def delete_test_resource(self, endpoint: str, resource_id: int):
        """
        Méthode utilitaire pour supprimer une ressource de test
        """
        response = self.client.delete(f"{endpoint}/{resource_id}", headers=self.headers)
        assert response.status_code in [200, 204]
        return response.json()

    def verify_required_fields(self, endpoint: str, data: dict, required_fields: list):
        """
        Vérifie que tous les champs requis sont bien obligatoires
        """
        for field in required_fields:
            invalid_data = data.copy()
            del invalid_data[field]
            response = self.client.post(endpoint, json=invalid_data, headers=self.headers)
            assert response.status_code == 422, f"Le champ {field} devrait être requis"

    def verify_unauthorized_access(self, endpoint: str, method: str = "get"):
        """
        Vérifie que l'accès non autorisé est bien géré
        """
        # Test sans token
        response = getattr(self.client, method)(endpoint)
        assert response.status_code == 401

        # Test avec token invalide
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = getattr(self.client, method)(endpoint, headers=invalid_headers)
        assert response.status_code == 401

    def create_test_boat(self, boat_data):
        """
        Crée un bateau de test et retourne ses données
        """
        return self.create_test_resource("/v1/boats", boat_data)

    def create_test_trip(self, trip_data, boat_id=None):
        """
        Crée une sortie de test et retourne ses données
        """
        if boat_id:
            trip_data["boat_id"] = boat_id
        return self.create_test_resource("/v1/trips", trip_data)

    def create_test_reservation(self, reservation_data, trip_id=None):
        """
        Crée une réservation de test et retourne ses données
        """
        if trip_id:
            reservation_data["trip_id"] = trip_id
        return self.create_test_resource("/v1/reservations", reservation_data)

    def create_test_log(self, log_data):
        """
        Crée un log de test et retourne ses données
        """
        return self.create_test_resource("/v1/logs", log_data)

    def assert_resource_exists(self, endpoint: str, resource_id: int):
        """
        Vérifie qu'une ressource existe
        """
        response = self.client.get(f"{endpoint}/{resource_id}", headers=self.headers)
        assert response.status_code == 200
        return response.json()

    def assert_resource_not_found(self, endpoint: str, resource_id: int):
        """
        Vérifie qu'une ressource n'existe pas
        """
        response = self.client.get(f"{endpoint}/{resource_id}", headers=self.headers)
        assert response.status_code == 404
