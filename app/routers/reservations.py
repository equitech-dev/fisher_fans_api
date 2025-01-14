from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationResponse

router = APIRouter(prefix="/v1/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponse, status_code=201)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get("/{id}", response_model=ReservationResponse)
def get_reservation(id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation
