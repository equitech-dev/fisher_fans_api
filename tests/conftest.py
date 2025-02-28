import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.enum import StatusEnum, BoatTypeEnum, MotorEnum, LicenseEnum

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "name": "Doe",
        "firstname": "John",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890",
        "status": StatusEnum.INDIVIDUAL.value,
        "boat_license": 123456789
    }

@pytest.fixture
def test_admin_user_data():
    return {
        "name": "Admin",
        "firstname": "Super",
        "email": "admin@example.com",
        "password": "admin123",
        "status": StatusEnum.INDIVIDUAL.value,
        "role": "admin"
    }

@pytest.fixture
def test_boat_data():
    return {
        "name": "Test Boat",
        "boat_type": BoatTypeEnum.OPEN.value,
        "description": "A test boat",
        "brand": "Test Brand",
        "fabrication_year": 2020,
        "photo_url": "http://example.com/boat.jpg",
        "license": LicenseEnum.COASTAL.value,
        "equipment": ["GPS", "RADIO"],
        "caution": 1000.0,
        "nb_passenger": 4,
        "nb_seat": 4,
        "port": "Test Port",
        "latitude": 43.296482,
        "longitude": 5.369780,
        "motor": MotorEnum.GASOLINE.value,
        "motor_power": 150
    }

@pytest.fixture
def test_trip_data():
    return {
        "title": "Test Trip",
        "description": "A test fishing trip",
        "practical_info": "Bring your gear",
        "trip_type": "DAILY",
        "pricing_type": "PER_PERSON",
        "dates": [{"start": "2025-02-10", "end": "2025-02-10"}],
        "schedules": [{"departure": "06:00:00", "arrival": "12:00:00"}],
        "nb_passengers": 4,
        "price": 100.0
    }

@pytest.fixture
def test_reservation_data():
    return {
        "reservation_date": "2025-02-10",
        "nb_seats": 2,
        "total_price": 200.0
    }

@pytest.fixture
def test_log_data():
    return {
        "fish_name": "Bass",
        "picture_url": "http://example.com/fish.jpg",
        "comment": "Nice catch!",
        "size": 45.5,
        "weight": 2.3,
        "location": "Mediterranean Sea",
        "catch_date": "2025-02-10",
        "released": True
    }

@pytest.fixture(scope="function")
def auth_headers(client, test_user_data):
    # Créer l'utilisateur
    response = client.post("/v1/users/", json=test_user_data)
    print(response.json())
    assert response.status_code == 201
    token = response.json()["token"]
    
    # Vérifier que le token est valide
    headers = {"Authorization": {token}}
    test_response = client.get("/v1/users/1/", headers=headers)
    assert test_response.status_code == 200
    
    return headers

@pytest.fixture(scope="function")
def admin_auth_headers(client, test_admin_user_data):
    # Créer l'admin
    response = client.post("/v1/users", json=test_admin_user_data)
    assert response.status_code == 201
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}
