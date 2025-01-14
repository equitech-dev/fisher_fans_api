from pydantic import BaseModel
from typing import Optional

class BoatBase(BaseModel):
    name: str
    boat_type: str
    motor: str
    capacity: int

class BoatCreate(BoatBase):
    owner_id: int

class BoatResponse(BoatBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
