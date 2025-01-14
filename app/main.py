import sys
import os
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, boats, trips, reservations, logs
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends
from typing_extensions import Annotated

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST_URL",), port=8000)
