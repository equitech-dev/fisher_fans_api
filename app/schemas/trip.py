from pydantic import BaseModel
from datetime import date
from typing import Optional

class TripBase(BaseModel):
    title: str
    trip_date: date
    price: float
    boat_id: int
    organizer_id: int

class TripCreate(TripBase):
    pass

class TripResponse(TripBase):
    id: int

    class Config:
        orm_mode = True
