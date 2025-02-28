import pytest
from datetime import datetime, timedelta
from tests.test_base import TestBase  # Changed from relative import to absolute import

class TestTripEndpoints:
    def setup_test_boat(self, client, auth_headers, test_boat_data):
        response = client.post("/v1/boats", json=test_boat_data, headers=auth_headers)
        assert response.status_code == 201
        return response.json()["id"]

    def test_create_trip_success(self, client, auth_headers, test_trip_data, test_boat_data):
        # Setup : créer un bateau d'abord
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {**test_trip_data, "boat_id": boat_id}
        
        response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == trip_data["title"]
        assert data["boat_id"] == boat_id
        assert isinstance(data["dates"], list)
        assert isinstance(data["schedules"], list)

    def test_create_trip_without_boat(self, client, auth_headers, test_trip_data):
        trip_data = {**test_trip_data, "boat_id": 99999}
        response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        assert response.status_code == 403
        assert "User can only create trips with their own boats" in response.json()["detail"]

    def test_create_trip_exceeded_capacity(self, client, auth_headers, test_trip_data, test_boat_data):
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {
            **test_trip_data,
            "boat_id": boat_id,
            "nb_passengers": test_boat_data["nb_passenger"] + 1
        }
        response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        assert response.status_code == 400
        assert "exceeds boat capacity" in response.json()["detail"]

    def test_create_trip_invalid_dates(self, client, auth_headers, test_trip_data, test_boat_data):
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {
            **test_trip_data,
            "boat_id": boat_id,
            "dates": [{"start": "2025-02-10", "end": "2025-02-09"}]  # end before start
        }
        response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Start date must be before end date" in response.json()["detail"]

    def test_get_trip_success(self, client, auth_headers, test_trip_data, test_boat_data):
        # Create a trip first
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {**test_trip_data, "boat_id": boat_id}
        create_response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        trip_id = create_response.json()["id"]
        
        # Get the trip
        response = client.get(f"/v1/trips/{trip_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == trip_data["title"]
        assert isinstance(data["dates"], list)
        assert isinstance(data["schedules"], list)

    def test_get_trip_not_found(self, client, auth_headers):
        response = client.get("/v1/trips/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_filter_trips_all_params(self, client, auth_headers):
        response = client.get("/v1/trips/filter", headers=auth_headers, params={
            "trip_type": "DAILY",
            "pricing_type": "PER_PERSON",
            "min_price": 50,
            "max_price": 150,
            "min_passengers": 2,
            "boat_id": 1,
            "start_date": "2025-02-10",
            "end_date": "2025-02-15",
            "start_time": "06:00:00",
            "end_time": "18:00:00"
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_trip_success(self, client, auth_headers, test_trip_data, test_boat_data):
        # Create initial trip
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {**test_trip_data, "boat_id": boat_id}
        create_response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        trip_id = create_response.json()["id"]
        
        # Update trip
        update_data = {
            "title": "Updated Trip",
            "price": 150.0,
            "dates": [{"start": "2025-03-10", "end": "2025-03-10"}]
        }
        response = client.put(f"/v1/trips/{trip_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["price"] == update_data["price"]

    def test_update_trip_unauthorized(self, client, auth_headers, test_trip_data, test_boat_data):
        # Create trip with first user
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {**test_trip_data, "boat_id": boat_id}
        create_response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        trip_id = create_response.json()["id"]
        
        # Create and login as second user
        second_user = {
            "name": "Smith",
            "firstname": "Jane",
            "email": "jane.smith@example.com",
            "password": "password123",
            "status": "individual"  # Changed from "particulier" to "individual"
        }
        client.post("/v1/users", json=second_user)
        login_response = client.post("/v1/login", data={
            "username": second_user["email"],
            "password": second_user["password"]
        })
        new_headers = {"Authorization": f"Bearer {login_response.json()['token']}"}
        
        # Try to update trip
        response = client.put(f"/v1/trips/{trip_id}", 
            json={"title": "Unauthorized Update"},
            headers=new_headers
        )
        assert response.status_code == 403

    def test_delete_trip_success(self, client, auth_headers, test_trip_data, test_boat_data):
        # Create trip
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {**test_trip_data, "boat_id": boat_id}
        create_response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        trip_id = create_response.json()["id"]
        
        # Delete trip
        response = client.delete(f"/v1/trips/{trip_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Verify deletion
        get_response = client.get(f"/v1/trips/{trip_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_trip_unauthorized(self, client, auth_headers, test_trip_data, test_boat_data):
        # Similar to update unauthorized test
        boat_id = self.setup_test_boat(client, auth_headers, test_boat_data)
        trip_data = {**test_trip_data, "boat_id": boat_id}
        create_response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        trip_id = create_response.json()["id"]
        
        # Create and login as second user
        second_user = {
            "name": "Smith",
            "firstname": "Jane",
            "email": "jane.delete@example.com",
            "password": "password123",
            "status": "individual"  # Changed from "particulier" to "individual"
        }
        client.post("/v1/users", json=second_user)
        login_response = client.post("/v1/login", data={
            "username": second_user["email"],
            "password": second_user["password"]
        })
        new_headers = {"Authorization": f"Bearer {login_response.json()['token']}"}
        
        response = client.delete(f"/v1/trips/{trip_id}", headers=new_headers)
        assert response.status_code == 403
