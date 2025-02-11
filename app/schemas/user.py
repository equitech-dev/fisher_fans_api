from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from app.models.enum import StatusEnum
from app.schemas.boat import BoatResponse
from app.schemas.trip import TripResponse
from app.schemas.reservation import ReservationResponse
from app.schemas.log import LogResponse

class UserBase(BaseModel):
    firstname: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    picture: Optional[str] = None
    boat_license: Optional[int] = None
    insurance: Optional[str] = None
    company_name: Optional[str] = None 
    siret: Optional[str] = None 
    rcs: Optional[str] = None 
    status: Optional[StatusEnum] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    pass

class UserInscriptionReurn(BaseModel):
    token: str

class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    picture: Optional[str] = None
    boat_license: Optional[int] = None
    insurance: Optional[str] = None
    company_name: Optional[str] = None
    siret: Optional[str] = None
    rcs: Optional[str] = None
    status: Optional[StatusEnum] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True

class UserFullProfile(BaseModel):
    id: int
    name: str
    firstname: str
    email: str
    phone: Optional[str]
    status: str
    boats: List[BoatResponse]
    trips: List[TripResponse]
    reservations: List[ReservationResponse]
    logs: List[LogResponse]

    class Config:
        from_attributes = True
