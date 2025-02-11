from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.reservation import Reservation
from app.models.trip import Trip
from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationUpdate
from app.dependencies import get_current_user
from app.models.enum import RoleEnum

router = APIRouter(prefix="/v1/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Vérifier que la sortie existe
    trip = db.query(Trip).filter(Trip.id == reservation.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Calculer le nombre total de places déjà réservées
    total_reserved = sum(r.nb_seats for r in db.query(Reservation).filter(
        Reservation.trip_id == reservation.trip_id,
        Reservation.reservation_date == reservation.reservation_date
    ).all())

    # Vérifier s'il reste assez de places
    if total_reserved + reservation.nb_seats > trip.nb_passengers:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough seats available. Only {trip.nb_passengers - total_reserved} seats left"
        )

    # Vérifier si la date de réservation est dans le futur
    if reservation.reservation_date < date.today():
        raise HTTPException(status_code=400, detail="Reservation date must be in the future")

    # Vérifier si la date de réservation correspond à une des dates du trip
    valid_dates = any(
        date.fromisoformat(trip_date["start"]) <= reservation.reservation_date <= date.fromisoformat(trip_date["end"])
        for trip_date in trip.dates
    )
    if not valid_dates:
        raise HTTPException(
            status_code=400, 
            detail="Reservation date must be within one of the trip's date ranges"
        )
    
    db_reservation = Reservation(
        **reservation.dict(),
        user_id=current_user.id
    )
    
    try:
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return db_reservation

@router.get("/filter", response_model=List[ReservationResponse])
def filter_reservations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    trip_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    min_date: Optional[date] = Query(None),
    max_date: Optional[date] = Query(None),
    min_seats: Optional[int] = Query(None),
    max_seats: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None)
):
    query = db.query(Reservation)

    # Filtrer par défaut sur l'utilisateur courant sauf si admin
    if current_user.role != RoleEnum.ADMIN:
        query = query.join(Trip).filter(
            (Reservation.user_id == current_user.id) | 
            (Trip.organizer_id == current_user.id)
        )
    elif user_id:
        query = query.filter(Reservation.user_id == user_id)

    if trip_id:
        query = query.filter(Reservation.trip_id == trip_id)
    if min_seats:
        query = query.filter(Reservation.nb_seats >= min_seats)
    if max_seats:
        query = query.filter(Reservation.nb_seats <= max_seats)
    if min_price:
        query = query.filter(Reservation.total_price >= min_price)
    if max_price:
        query = query.filter(Reservation.total_price <= max_price)

    return query.all()

@router.put("/{id}", response_model=ReservationResponse)
def update_reservation(
    id: int,
    reservation_update: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Vérifier les droits d'accès
    if db_reservation.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to modify this reservation")

    if reservation_update.nb_seats:
        # Recalculer le nombre de places disponibles
        trip = db.query(Trip).filter(Trip.id == db_reservation.trip_id).first()
        total_reserved = sum(r.nb_seats for r in db.query(Reservation).filter(
            Reservation.trip_id == db_reservation.trip_id,
            Reservation.id != id
        ).all())

        if total_reserved + reservation_update.nb_seats > trip.nb_passengers:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough seats available. Only {trip.nb_passengers - total_reserved} seats left"
            )
    if reservation_update.reservation_date:
        # Vérifier si la date de réservation est dans le futur
        if reservation_update.reservation_date < date.today():
            raise HTTPException(status_code=400, detail="Reservation date must be in the future")

        # Vérifier si la date de réservation correspond à une des dates du trip
        trip = db.query(Trip).filter(Trip.id == db_reservation.trip_id).first()
        valid_dates = any(
            date.fromisoformat(trip_date["start"]) <= reservation_update.reservation_date <= date.fromisoformat(trip_date["end"])
            for trip_date in trip.dates
        )
        if not valid_dates:
            raise HTTPException(
                status_code=400, 
                detail="Reservation date must be within one of the trip's date ranges"
            )
    for key, value in reservation_update.dict(exclude_unset=True).items():
        setattr(db_reservation, key, value)

    try:
        db.commit()
        db.refresh(db_reservation)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return db_reservation

@router.delete("/{id}")
def delete_reservation(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Vérifier les droits d'accès
    if db_reservation.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to delete this reservation")

    try:
        db.delete(db_reservation)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Reservation successfully deleted"}

@router.get("/{id}", response_model=ReservationResponse)
def get_reservation(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    trip = db.query(Trip).filter(Trip.id == db_reservation.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Vérifier les droits d'accès
    if (db_reservation.user_id != current_user.id and 
        current_user.role != RoleEnum.ADMIN and 
        trip.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this reservation")

    return db_reservation