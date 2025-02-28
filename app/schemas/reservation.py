from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReservationBase(BaseModel):
    trip_id: int
    reservation_date: date
    nb_seats: int
    total_price: float

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class ReservationUpdate(BaseModel):
    nb_seats: Optional[int] = None
    reservation_date: Optional[date] = None

    class Config:
        from_attributes = True
