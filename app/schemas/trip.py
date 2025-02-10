from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date, time
from app.models.enum import TripTypeEnum, PricingTypeEnum

class TripDate(BaseModel):
    start: date
    end: date

class TripSchedule(BaseModel):
    departure: time
    arrival: time

class TripBase(BaseModel):
    title: str
    practical_info: Optional[str] = None
    trip_type: TripTypeEnum
    pricing_type: PricingTypeEnum
    dates: List[TripDate]
    schedules: List[TripSchedule]
    nb_passengers: int
    price: float
    boat_id: int

class TripCreate(TripBase):
    pass

class TripResponse(TripBase):
    id: int
    organizer_id: int

    class Config:
        from_attributes = True

class TripUpdate(BaseModel):
    title: Optional[str] = None
    practical_info: Optional[str] = None
    trip_type: Optional[TripTypeEnum] = None
    pricing_type: Optional[PricingTypeEnum] = None
    dates: Optional[List[TripDate]] = None
    schedules: Optional[List[TripSchedule]] = None
    nb_passengers: Optional[int] = None
    price: Optional[float] = None
    boat_id: Optional[int] = None

    class Config:
        from_attributes = True
