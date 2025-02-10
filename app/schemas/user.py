from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from app.models.enum import StatusEnum

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
