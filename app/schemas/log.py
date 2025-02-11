from pydantic import BaseModel
from datetime import date
from typing import Optional

class LogBase(BaseModel):
    fish_name: str
    picture_url: Optional[str] = None
    comment: Optional[str] = None
    size: Optional[float] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    catch_date: date
    released: bool = False

class LogCreate(LogBase):
    pass

class LogUpdate(BaseModel):
    fish_name: Optional[str] = None
    picture_url: Optional[str] = None
    comment: Optional[str] = None
    size: Optional[float] = None
    weight: Optional[float] = None
    location: Optional[str] = None
    catch_date: Optional[date] = None
    released: Optional[bool] = None

class LogResponse(LogBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
