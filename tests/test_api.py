import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/v1/users", json={
        "name": "Doe",
        "firstname": "John",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "1234567890",
        "status": "active"
    })
    assert response.status_code == 200

def test_get_user():
    response = client.get("/v1/users/1")
    assert response.status_code == 200

def test_update_user():
    response = client.put("/v1/users/1", json={
        "name": "Doe",
        "firstname": "John",
        "email": "john.doe@example.com",
        "password": "newpassword",
        "phone": "0987654321",
        "status": "active"
    })
    assert response.status_code == 200

def test_delete_user():
    response = client.delete("/v1/users/1")
    assert response.status_code == 200

def test_create_boat():
    response = client.post("/v1/boats", json={
        "name": "Fishing Boat",
        "boat_type": "Fishing",
        "motor": "Yamaha",
        "capacity": 4,
        "owner_id": 1
    })
    assert response.status_code == 200

def test_get_boat():
    response = client.get("/v1/boats/1")
    assert response.status_code == 200

def test_update_boat():
    response = client.put("/v1/boats/1", json={
        "name": "Fishing Boat",
        "boat_type": "Fishing",
        "motor": "Yamaha",
        "capacity": 4,
        "owner_id": 1
    })
    assert response.status_code == 200

def test_delete_boat():
    response = client.delete("/v1/boats/1")
    assert response.status_code == 200

def test_create_trip():
    response = client.post("/v1/trips", json={
        "title": "Morning Fishing Trip",
        "description": "A relaxing morning fishing trip.",
        "nb_passengers": 4,  # Modifié de nb_passenger à nb_passengers
        "price": 100.0,
        "trip_type": "DAILY",        # Valeur corrigée
        "pricing_type": "PER_PERSON",  # Valeur corrigée
        "dates": [{"start": "2025-02-10", "end": "2025-02-10"}],
        "schedules": [{"departure": "06:00:00", "arrival": "12:00:00"}],
        "boat_id": 1
    })
    assert response.status_code == 200

def test_get_trip():
    response = client.get("/v1/trips/1")
    assert response.status_code == 200

def test_update_trip():
    response = client.put("/v1/trips/1", json={
        "title": "Morning Fishing Trip",
        "description": "A relaxing morning fishing trip.",
        "nb_passengers": 4,  # Modifié de nb_passenger à nb_passengers
        "price": 100.0,
        "trip_type": "DAILY",        # Valeur corrigée
        "pricing_type": "PER_PERSON",  # Valeur corrigée
        "dates": [{"start": "2025-02-10", "end": "2025-02-10"}],
        "schedules": [{"departure": "06:00:00", "arrival": "12:00:00"}],
        "boat_id": 1
    })
    assert response.status_code == 200

def test_delete_trip():
    response = client.delete("/v1/trips/1")
    assert response.status_code == 200

def test_create_reservation():
    response = client.post("/v1/reservations", json={
        "nb_places": 2,
        "total_price": 200.0,
        "user_id": 1,
        "trip_id": 1
    })
    assert response.status_code == 200

def test_get_reservation():
    response = client.get("/v1/reservations/1")
    assert response.status_code == 200

def test_update_reservation():
    response = client.put("/v1/reservations/1", json={
        "nb_places": 2,
        "total_price": 200.0,
        "user_id": 1,
        "trip_id": 1
    })
    assert response.status_code == 200

def test_delete_reservation():
    response = client.delete("/v1/reservations/1")
    assert response.status_code == 200

def test_create_log():
    response = client.post("/v1/logs", json={
        "fish": "Salmon",
        "picture": "salmon.jpg",
        "comment": "Caught a big one!",
        "size": 5.0,
        "weight": 10.0,
        "place": "Lake",
        "kept": 1,
        "user_id": 1
    })
    assert response.status_code == 200

def test_get_log():
    response = client.get("/v1/logs/1")
    assert response.status_code == 200

def test_update_log():
    response = client.put("/v1/logs/1", json={
        "fish": "Salmon",
        "picture": "salmon.jpg",
        "comment": "Caught a big one!",
        "size": 5.0,
        "weight": 10.0,
        "place": "Lake",
        "kept": 1,
        "user_id": 1
    })
    assert response.status_code == 200

def test_delete_log():
    response = client.delete("/v1/logs/1")
    assert response.status_code == 200
