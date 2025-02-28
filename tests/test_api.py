import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
# Ajout du token dans les headers pour accéder aux endpoints protégés
client.headers.update({"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QHRlc3QuY29tIiwic3RhdHVzIjoicGFydGljdWxpZXIiLCJleHAiOjE3Mzk0MzkwODcsImFwaV9rZXkiOiJGRl9BUEkifQ.CnAAUz2KXlQSlYk7lyfmiT2oA1MH7KyErRMyX0jWn5A"})

# ----- Tests pour l'utilisateur -----
def test_create_user_valid():
    response = client.post("/v1/users", json={
        "name": "Doe",
        "firstname": "John",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "1234567890",
        "status": "particulier"  # enum: particulier ou professionnel
    })
    assert response.status_code == 200

def test_create_user_invalid_missing_field():
    response = client.post("/v1/users", json={
        "name": "Doe",
        "firstname": "John",
        # email absent
        "password": "password",
        "phone": "1234567890",
        "status": "particulier"
    })
    assert response.status_code != 200

def test_get_user_valid():
    response = client.get("/v1/users/1")
    assert response.status_code == 200

def test_get_user_not_found():
    response = client.get("/v1/users/99999")
    assert response.status_code == 404

def test_update_user_valid():
    response = client.put("/v1/users/1", json={
        "name": "Doe",
        "firstname": "John",
        "email": "john.doe@example.com",
        "password": "newpassword",
        "phone": "0987654321",
        "status": "particulier"
    })
    assert response.status_code == 200

def test_delete_user_valid():
    response = client.delete("/v1/users/1")
    assert response.status_code == 200

# ----- Tests pour le bateau -----
def test_create_boat_valid():
    response = client.post("/v1/boats", json={
        "name": "Fishing Boat",
        "boat_type": "OPEN",  # valeur de BoatTypeEnum attendue
        "description": "A sturdy fishing boat",
        "brand": "Yamaha",
        "fabrication_year": 2015,
        "photo_url": "http://photo.url/boat.jpg",
        "license": "COASTAL",
        "equipment": ["GPS", "RADIO"],
        "caution": 1000.0,
        "nb_passenger": 4,
        "nb_seat": 4,
        "port": "Marina",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "motor": "GASOLINE",
        "motor_power": 200
    })
    assert response.status_code == 200

def test_create_boat_invalid_missing_field():
    # Manque le champ "brand"
    response = client.post("/v1/boats", json={
        "name": "Boat",
        "boat_type": "OPEN",
        "description": "Test boat",
        "fabrication_year": 2010,
        "photo_url": "http://photo.url/boat.jpg",
        "license": "COASTAL",
        "equipment": ["GPS"],
        "caution": 500.0,
        "nb_passenger": 4,
        "nb_seat": 4,
        "port": "Marina",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "motor": "GASOLINE",
        "motor_power": 150
    })
    assert response.status_code != 200

def test_get_boat_valid():
    response = client.get("/v1/boats/1")
    assert response.status_code == 200

def test_get_boat_not_found():
    response = client.get("/v1/boats/99999")
    assert response.status_code == 404

def test_update_boat_valid():
    response = client.put("/v1/boats/1", json={
        "name": "Fishing Boat Updated",
        "boat_type": "OPEN",
        "description": "An updated boat description",
        "brand": "Yamaha",
        "fabrication_year": 2016,
        "photo_url": "http://photo.url/boat_updated.jpg",
        "license": "COASTAL",
        "equipment": ["GPS", "RADIO"],
        "caution": 1200.0,
        "nb_passenger": 4,
        "nb_seat": 4,
        "port": "Marina",
        "latitude": 48.8567,
        "longitude": 2.3523,
        "motor": "GASOLINE",
        "motor_power": 220
    })
    assert response.status_code == 200

def test_delete_boat_valid():
    response = client.delete("/v1/boats/1")
    assert response.status_code == 200

# ----- Tests pour le trip -----
def test_create_trip_valid():
    # Pré-requis : création d'un bateau pour l'utilisateur
    boat_response = client.post("/v1/boats", json={
        "name": "Trip Boat",
        "boat_type": "OPEN",
        "description": "Boat for trip",
        "brand": "Yamaha",
        "fabrication_year": 2015,
        "photo_url": "http://photo.url/boat_trip.jpg",
        "license": "COASTAL",
        "equipment": ["GPS"],
        "caution": 800.0,
        "nb_passenger": 6,
        "nb_seat": 6,
        "port": "Marina",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "motor": "GASOLINE",
        "motor_power": 180
    })
    boat_id = boat_response.json().get("id")
    response = client.post("/v1/trips", json={
        "title": "Morning Fishing Trip",
        "description": "A relaxing morning fishing trip.",
        "nb_passengers": 4,
        "price": 100.0,
        "trip_type": "DAILY",
        "pricing_type": "PER_PERSON",
        "dates": [{"start": "2025-02-10", "end": "2025-02-10"}],
        "schedules": [{"departure": "06:00:00", "arrival": "12:00:00"}],
        "boat_id": boat_id
    })
    assert response.status_code == 200

def test_create_trip_fail_no_boat_owned():
    response = client.post("/v1/trips", json={
        "title": "Trip without boat",
        "description": "Should fail",
        "nb_passengers": 4,
        "price": 100.0,
        "trip_type": "DAILY",
        "pricing_type": "PER_PERSON",
        "dates": [{"start": "2025-02-10", "end": "2025-02-10"}],
        "schedules": [{"departure": "06:00:00", "arrival": "12:00:00"}],
        "boat_id": 99999
    })
    assert response.status_code == 403

def test_get_trip_valid():
    response = client.get("/v1/trips/1")
    assert response.status_code == 200

def test_get_trip_not_found():
    response = client.get("/v1/trips/99999")
    assert response.status_code == 404

def test_update_trip_valid():
    response = client.put("/v1/trips/1", json={
        "title": "Morning Fishing Trip Updated",
        "description": "An updated relaxing morning fishing trip.",
        "nb_passengers": 4,
        "price": 120.0,
        "trip_type": "DAILY",
        "pricing_type": "PER_PERSON",
        "dates": [{"start": "2025-02-10", "end": "2025-02-10"}],
        "schedules": [{"departure": "06:00:00", "arrival": "12:00:00"}],
        "boat_id": 1
    })
    assert response.status_code == 200

def test_update_trip_fail_invalid_boat():
    response = client.put("/v1/trips/1", json={
        "boat_id": 99999
    })
    assert response.status_code == 403

def test_filter_trip():
    response = client.get("/v1/trips/filter", params={
        "trip_type": "DAILY",
        "pricing_type": "PER_PERSON",
        "min_price": 50,
        "max_price": 150,
        "min_passengers": 1,
        "boat_id": 1,
        "start_date": "2025-02-10",
        "end_date": "2025-02-10",
        "start_time": "06:00:00",
        "end_time": "12:00:00"
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_delete_trip_valid():
    response = client.delete("/v1/trips/1")
    assert response.status_code == 200

# ... d'autres tests pour couvrir le reste des branches si nécessaire ...
