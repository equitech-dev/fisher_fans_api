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
not_found_error_resa = "Reservation not found"
"""
Endpoints for managing reservations
"""

@router.post("/", response_model=ReservationResponse, summary="Create a new reservation")
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Create a new reservation

    Args:
        reservation (ReservationCreate): The reservation data
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        ReservationResponse: The created reservation
    """
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

@router.get("/filter", response_model=List[ReservationResponse], summary="Filter reservations")
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
    """
    Filter reservations

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).
        trip_id (Optional[int], optional): Filter by trip id. Defaults to None.
        user_id (Optional[int], optional): Filter by user id. Defaults to None.
        min_date (Optional[date], optional): Filter by minimum date. Defaults to None.
        max_date (Optional[date], optional): Filter by maximum date. Defaults to None.
        min_seats (Optional[int], optional): Filter by minimum seats. Defaults to None.
        max_seats (Optional[int], optional): Filter by maximum seats. Defaults to None.
        min_price (Optional[float], optional): Filter by minimum price. Defaults to None.
        max_price (Optional[float], optional): Filter by maximum price. Defaults to None.

    Returns:
        List[ReservationResponse]: The filtered reservations
    """
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

@router.put("/{id}", response_model=ReservationResponse, summary="Update a reservation")
def update_reservation(
    id: int,
    reservation_update: ReservationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update a reservation

    Args:
        id (int): The reservation id
        reservation_update (ReservationUpdate): The updated reservation data
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        ReservationResponse: The updated reservation
    """
    db_reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail=not_found_error_resa)

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

@router.delete("/{id}", summary="Delete a reservation")
def delete_reservation(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a reservation

    Args:
        id (int): The reservation id
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        [type]: [description]
    """
    db_reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail=not_found_error_resa)

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

@router.get("/{id}", response_model=ReservationResponse, summary="Get a reservation")
def get_reservation(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Get a reservation

    Args:
        id (int): The reservation id
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (User, optional): The current user. Defaults to Depends(get_current_user).

    Returns:
        ReservationResponse: The reservation
    """
    db_reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail=not_found_error_resa)

    trip = db.query(Trip).filter(Trip.id == db_reservation.trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")