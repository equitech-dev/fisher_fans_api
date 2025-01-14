from pydantic import BaseModel
from typing import Optional

class ReservationBase(BaseModel):
    user_id: int
    trip_id: int
    number_of_seats: int
    total_price: float

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int

    class Config:
        orm_mode = True
