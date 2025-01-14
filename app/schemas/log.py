from pydantic import BaseModel
from datetime import datetime

class LogBase(BaseModel):
    fish_name: str
    size: float
    weight: float
    location: str
    date_caught: datetime
    released: bool
    user_id: int

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    id: int

    class Config:
        from_attributes = True
