from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripResponse

router = APIRouter(prefix="/v1/trips", tags=["Trips"])

@router.post("/", response_model=TripResponse, status_code=201)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = Trip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.get("/{id}", response_model=TripResponse)
def get_trip(id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip
