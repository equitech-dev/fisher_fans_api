from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.trip import Trip
from app.models.boat import Boat
from app.schemas.trip import TripCreate, TripResponse, TripUpdate
from app.dependencies import get_current_user
from app.models.enum import RoleEnum, TripTypeEnum, PricingTypeEnum
from datetime import date, time
from app.schemas.trip import TripDate, TripSchedule

router = APIRouter(prefix="/v1/trips", tags=["Trips"])
@router.post("/", response_model=TripResponse, summary="Create a trip")
def create_trip(trip: TripCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Create a trip.

    Args:
    - trip (TripCreate): Informations du trip.

    Returns:
    - TripResponse: Created trip.
    """
    # Vérifier que l'utilisateur possède au moins un bateau
    user_boats = db.query(Boat).filter(Boat.owner_id == current_user.id).all()
    if not user_boats:
        raise HTTPException(status_code=403, detail="User must own a boat to create trips")
    
    # Vérifier que le bateau appartient à l'utilisateur
    boat = db.query(Boat).filter(Boat.id == trip.boat_id, Boat.owner_id == current_user.id).first()
    if not boat:
        raise HTTPException(status_code=403, detail="User can only create trips with their own boats")

    # Vérifier que le nombre de passagers ne dépasse pas la capacité du bateau
    if trip.nb_passengers > boat.nb_passenger:
        raise HTTPException(
            status_code=400, 
            detail=f"Number of passengers ({trip.nb_passengers}) exceeds boat capacity ({boat.nb_passenger})"
        )
    trip_data = trip.dict()
    # Vérification des dates et conversion conditionnelle
    for item in trip_data["dates"]:
        # Si l'objet possède isoformat, c'est un objet date; sinon, c'est une chaîne déjà formatée
        start_val = item["start"].isoformat() if hasattr(item["start"], "isoformat") else item["start"]
        end_val = item["end"].isoformat() if hasattr(item["end"], "isoformat") else item["end"]
        if start_val >= end_val:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
    trip_data["dates"] = [
        {
            "start": item["start"].isoformat() if hasattr(item["start"], "isoformat") else item["start"],
            "end": item["end"].isoformat() if hasattr(item["end"], "isoformat") else item["end"]
        } 
        for item in trip_data["dates"]
    ]
    trip_data["schedules"] = [
        {
            "departure": item["departure"].isoformat() if hasattr(item["departure"], "isoformat") else item["departure"],
            "arrival": item["arrival"].isoformat() if hasattr(item["arrival"], "isoformat") else item["arrival"]
        }
        for item in trip_data["schedules"]
    ]

    try:
        db_trip = Trip(**trip_data, organizer_id=current_user.id)
        db.add(db_trip)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Trip creation failed due to an internal error " + str(e))
    db.refresh(db_trip)
    return db_trip

@router.get("/filter", response_model=List[TripResponse], summary="Filter trips")
def filter_trips(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    trip_type: Optional[TripTypeEnum] = Query(None),
    pricing_type: Optional[PricingTypeEnum] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_passengers: Optional[int] = Query(None),
    boat_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    start_time: Optional[time] = Query(None),
    end_time: Optional[time] = Query(None),
):
    """
    Filter trips based on multiple criteria.

    Args:
    - trip_type (TripTypeEnum): Type of trip.
    - pricing_type (PricingTypeEnum): Pricing type.
    - min_price (int): Minimum price.
    - max_price (int): Maximum price.
    - min_passengers (int): Minimum number of passengers.
    - boat_id (int): Boat ID.
    - start_date (date): Start date.
    - end_date (date): End date.
    - start_time (time): Start time.
    - end_time (time): End time.

    Returns:
    - List[TripResponse]: List of filtered trips.
    """
    query = db.query(Trip)
    if current_user.role != RoleEnum.ADMIN:
        query = query.filter(Trip.organizer_id == current_user.id)
        
    if trip_type:
        query = query.filter(Trip.trip_type == trip_type)
    if min_price is not None:
        query = query.filter(Trip.price >= min_price)
    if max_price is not None:
        query = query.filter(Trip.price <= max_price)
    if min_passengers is not None:
        query = query.filter(Trip.nb_passengers >= min_passengers)
    if boat_id:
        query = query.filter(Trip.boat_id == boat_id)
    if pricing_type:
        query = query.filter(Trip.pricing_type == pricing_type)
    if start_date:
        query = query.filter(Trip.dates.any(start=start_date))
    if end_date:
        query = query.filter(Trip.dates.any(end=end_date))
    if start_time:
        query = query.filter(Trip.schedules.any(departure=start_time))
    if end_time:
        query = query.filter(Trip.schedules.any(arrival=end_time))
    
    trips = query.all()
    
    # Convert dates and schedules back to objects
    for trip in trips:
        trip.dates = [
            TripDate(start=date.fromisoformat(item["start"]), end=date.fromisoformat(item["end"]))
            for item in trip.dates
        ]
        trip.schedules = [
            TripSchedule(departure=time.fromisoformat(item["departure"]), arrival=time.fromisoformat(item["arrival"]))
            for item in trip.schedules
        ]
    
    return trips

@router.get("/{id}", response_model=TripResponse, summary="Get a trip")
def get_trip(
    id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get a trip.

    Args:
    - id (int): Trip ID.

    Returns:
    - TripResponse: Trip.
    """
    trip = db.query(Trip).filter(Trip.id == id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    try:
        trip_dates = [
            TripDate(start=date.fromisoformat(item["start"]), end=date.fromisoformat(item["end"]))
            for item in trip.dates
        ]
        trip_schedules = [
            TripSchedule(departure=time.fromisoformat(item["departure"]), arrival=time.fromisoformat(item["arrival"]))
            for item in trip.schedules
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error converting trip dates or schedules: " + str(e))
    
    trip.dates = trip_dates
    trip.schedules = trip_schedules
    return trip

@router.put("/{id}", response_model=TripResponse, summary="Update a trip")
def update_trip(
    id: int, 
    trip_update: TripUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    """
    Update a trip.

    Args:
    - id (int): Trip ID.
    - trip_update (TripUpdate): Updated trip information.

    Returns:
    - TripResponse: Updated trip.
    """
    trip = db.query(Trip).filter(Trip.id == id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Vérifier que l'utilisateur est l'organisateur ou un admin
    if trip.organizer_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Only the organizer or admin can update the trip")

    # Si le nombre de passagers est modifié, vérifier la capacité du bateau
    if trip_update.nb_passengers is not None:
        boat = db.query(Boat).filter(Boat.id == trip.boat_id).first()
        if trip_update.nb_passengers > boat.nb_passenger:
            raise HTTPException(
                status_code=400, 
                detail=f"Number of passengers ({trip_update.nb_passengers}) exceeds boat capacity ({boat.nb_passenger})"
            )

    # Si un nouveau bateau est spécifié, vérifier qu'il appartient à l'utilisateur
    if trip_update.boat_id:
        boat = db.query(Boat).filter(Boat.id == trip_update.boat_id, Boat.owner_id == current_user.id).first()
        if not boat:
            raise HTTPException(status_code=403, detail="Can only use owned boats")
        # Vérifier la capacité avec le nouveau bateau
        if trip.nb_passengers > boat.nb_passenger:
            raise HTTPException(
                status_code=400, 
                detail=f"Current number of passengers ({trip.nb_passengers}) exceeds new boat capacity ({boat.nb_passenger})"
            )

    for key, value in trip_update.dict(exclude_unset=True).items():
        # Convertir les Enum en leur valeur string pour les types trip_type et pricing_type
        if key in ["trip_type", "pricing_type"] and hasattr(value, "value"):
            value = value.value
        # Conversion des dates et horaires en chaînes ISO
