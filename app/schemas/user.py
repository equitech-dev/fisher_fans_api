from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    boats: Optional[List[int]] = []

    class Config:
        from_attributes = True
