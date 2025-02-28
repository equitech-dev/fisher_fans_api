from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models.user import User
from .models.boat import Boat
from .models.trip import Trip
from .models.reservation import Reservation
from .models.log import Log
import json
import time

def wait_for_db():
    while True:
        try:
            get_db()
            print("Database is ready!")
            break
        except Exception as e:
            print("Waiting for database to be ready...")
            time.sleep(5)

def init_db():
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)

    # Load data from JSON files
    users_data = load_data_from_json('data/users.json')
    boats_data = load_data_from_json('data/boats.json')
    trips_data = load_data_from_json('data/trips.json')
    reservations_data = load_data_from_json('data/reservations.json')
    logs_data = load_data_from_json('data/logs.json')

    # Add users from JSON
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        db.commit()

    # Add boats from JSON
    for boat_data in boats_data:
        boat = Boat(**boat_data)
        db.add(boat)
        db.commit()

    # Add trips from JSON
    for trip_data in trips_data:
        trip = Trip(**trip_data)
        db.add(trip)
        db.commit()

    # Add reservations from JSON
    for reservation_data in reservations_data:
        reservation = Reservation(**reservation_data)
        db.add(reservation)
        db.commit()

    # Add logs from JSON
    for log_data in logs_data:
        log = Log(**log_data)
        db.add(log)
        db.commit()

    db.close()

def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    init_db()