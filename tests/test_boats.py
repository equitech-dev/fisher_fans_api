import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_base import TestBase

class TestBoatEndpoints(TestBase):
    def test_create_boat_success(self, test_boat_data):
        response = self.client.post("/v1/boats", json=test_boat_data, headers=self.headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == test_boat_data["name"]
        assert isinstance(data["equipment"], list)

    def test_create_boat_unauthorized(self, test_boat_data):
        response = self.client.post("/v1/boats", json=test_boat_data)
        assert response.status_code == 401

    @pytest.mark.parametrize("field", ["name", "boat_type", "nb_passenger"])
    def test_create_boat_missing_required(self, test_boat_data, field):
        data = test_boat_data.copy()
        del data[field]
        response = self.client.post("/v1/boats", json=data, headers=self.headers)
        assert response.status_code == 422

    def test_get_boat_success(self, test_boat_data):
        # Create a boat first
        create_response = self.client.post("/v1/boats", json=test_boat_data, headers=self.headers)
        boat_id = create_response.json()["id"]
        
        # Get the boat
        response = self.client.get(f"/v1/boats/{boat_id}", headers=self.headers)
        assert response.status_code == 200
        assert response.json()["name"] == test_boat_data["name"]

    def test_update_boat_success(self, test_boat_data):
        # Create a boat first
        create_response = self.client.post("/v1/boats", json=test_boat_data, headers=self.headers)
        boat_id = create_response.json()["id"]
        
        # Update the boat
        update_data = {"name": "Updated Boat Name"}
        response = self.client.put(f"/v1/boats/{boat_id}", json=update_data, headers=self.headers)
        assert response.status_code == 200
        assert response.json()["name"] == update_data["name"]

    def test_delete_boat_success(self, test_boat_data):
        # Create a boat first
        create_response = self.client.post("/v1/boats", json=test_boat_data, headers=self.headers)
        boat_id = create_response.json()["id"]
        
        # Delete the boat
        response = self.client.delete(f"/v1/boats/{boat_id}", headers=self.headers)
        assert response.status_code == 200

    def test_filter_boats(self):
        response = self.client.get("/v1/boats/filter", headers=self.headers, params={
            "boat_type": "OPEN",
            "min_passenger": 2,
            "max_passenger": 8
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)
