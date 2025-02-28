import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.boat import Boat
from app.models.trip import Trip
from app.models.reservation import Reservation
from app.models.log import Log

DATA_DIR = "data"

# Fonction pour charger un fichier JSON
def load_json(filename):
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Fonction pour insérer les données en base
def insert_data():
    db: Session = SessionLocal()

    try:
        print("📥 Suppression des anciennes données dans le bon ordre...")

        # 1️⃣ Supprimer les dépendances (tables enfants)
        db.query(Log).delete()
        db.query(Reservation).delete()
        db.query(Trip).delete()
        db.query(Boat).delete()

        # 2️⃣ Ensuite, supprimer les utilisateurs (table parent)
        db.query(User).delete()

        db.commit()
        print("✅ Suppression réussie !")

        print("📥 Insertion des nouveaux utilisateurs...")
        users = load_json("users.json")
        for user in users:
            existing_user = db.query(User).filter(User.id == user["id"]).first()
            if not existing_user:
                db.add(User(**user))

        print("🚤 Insertion des bateaux...")
        boats = load_json("boats.json")
        for boat in boats:
            existing_boat = db.query(Boat).filter(Boat.id == boat["id"]).first()
            if not existing_boat:
                db.add(Boat(**boat))

        print("⛵ Insertion des voyages...")
        trips = load_json("trips.json")
        for trip in trips:
            existing_trip = db.query(Trip).filter(Trip.id == trip["id"]).first()
            if not existing_trip:
                db.add(Trip(**trip))

        print("📝 Insertion des réservations...")
        reservations = load_json("reservations.json")
        for reservation in reservations:
            existing_reservation = db.query(Reservation).filter(Reservation.id == reservation["id"]).first()
            if not existing_reservation:
                db.add(Reservation(**reservation))

        print("🎣 Insertion des logs de pêche...")
        logs = load_json("logs.json")
        for log in logs:
            existing_log = db.query(Log).filter(Log.id == log["id"]).first()
            if not existing_log:
                db.add(Log(**log))

        db.commit()
        print("✅ Données insérées avec succès !")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'insertion des données : {e}")

    finally:
        db.close()

if __name__ == "__main__":
    insert_data()
