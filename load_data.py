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

def insert_data():
    """Insère les données dans la base après avoir supprimé les anciennes."""
    with SessionLocal() as db:
        try:
            clear_database(db)

            data_files = {
                "users": (User, "id"),
                "boats": (Boat, "id"),
                "trips": (Trip, "id"),
                "reservations": (Reservation, "id"),
                "logs": (Log, "id"),
            }

            for file, (model, key) in data_files.items():
                insert_if_not_exists(db, file, model, key)

            db.commit()
            print("✅ Données insérées avec succès !")

        except Exception as e:
            db.rollback()
            print(f"❌ Erreur lors de l'insertion des données : {e}")


def clear_database(db: Session):
    """Supprime les anciennes données en respectant l'ordre des dépendances."""
    print("📥 Suppression des anciennes données dans le bon ordre...")

    for model in [Log, Reservation, Trip, Boat, User]:  # Ordre logique de suppression
        db.query(model).delete()

    db.commit()
    print("✅ Suppression réussie !")


def insert_if_not_exists(db: Session, file_name: str, model, key: str):
    """Insère les données depuis un fichier JSON si elles n'existent pas déjà."""
    print(f"📥 Insertion des {file_name}...")

    data = load_json(f"{file_name}.json")
    for entry in data:
        if not db.query(model).filter(getattr(model, key) == entry[key]).first():
            db.add(model(**entry))

if __name__ == "__main__":
    insert_data()
