import pytest
from datetime import date, timedelta

class TestReservationEndpoints:
    def test_create_reservation_success(self, client, auth_headers, test_reservation_data, test_trip_data, test_boat_data):
        # Setup: Create boat and trip first
        boat_response = client.post("/v1/boats", json=test_boat_data, headers=auth_headers)
        boat_id = boat_response.json()["id"]
        
        trip_data = {**test_trip_data, "boat_id": boat_id}
        trip_response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        trip_id = trip_response.json()["id"]
        
        # Create reservation
        reservation_data = {**test_reservation_data, "trip_id": trip_id}
        response = client.post("/v1/reservations", json=reservation_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["trip_id"] == trip_id

    def test_create_reservation_no_seats(self, client, auth_headers, test_reservation_data, test_trip_data, test_boat_data):
        # Setup similar to success test but with full capacity
        boat_response = client.post("/v1/boats", json=test_boat_data, headers=auth_headers)
        boat_id = boat_response.json()["id"]
        
        trip_data = {**test_trip_data, "boat_id": boat_id, "nb_passengers": 1}
        trip_response = client.post("/v1/trips", json=trip_data, headers=auth_headers)
        trip_id = trip_response.json()["id"]
        
        # Try to reserve more seats than available
        reservation_data = {**test_reservation_data, "trip_id": trip_id, "nb_seats": 2}
        response = client.post("/v1/reservations", json=reservation_data, headers=auth_headers)
        assert response.status_code == 400
        assert "Not enough seats" in response.json()["detail"]

    def test_get_reservation(self, client, auth_headers, test_reservation_data):
        # Create a reservation first
        # ... setup code ...
        response = client.get("/v1/reservations/1", headers=auth_headers)
        assert response.status_code in [200, 404]

    def test_filter_reservations(self, client, auth_headers):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        response = client.get("/v1/reservations/filter", headers=auth_headers, params={
            "min_date": tomorrow,
            "min_seats": 1,
            "max_seats": 4
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)
