from typing_extensions import Annotated
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, boats, trips, reservations, logs, auth  # Ajoutez auth
from app.init_db import init_db
import uvicorn
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import Depends
import sys
import os

# Add the parent directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add the current directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="Fisher Fans API",
    description="API pour gérer les utilisateurs, bateaux, sorties de pêche, réservations et carnets de pêche.",
    version="1.0.0"
)

db_dependecy = Annotated[Session, Depends(get_db)]
# Crée les tables dans la BDD
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(boats.router)
app.include_router(trips.router)
app.include_router(reservations.router)
app.include_router(logs.router)
app.include_router(auth.router)  # Ajoutez le routeur d'authentification

if __name__ == "__main__":
    get_db()
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)