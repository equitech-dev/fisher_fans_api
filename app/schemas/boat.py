from typing import List, Optional
from pydantic import BaseModel, field_validator
from app.models.enum import BoatTypeEnum, LicenseEnum, EquipmentEnum, MotorEnum
from pydantic.utils import GetterDict

# Mise à jour du modèle de base avec les enums
class BoatBase(BaseModel):
    name: str
    boat_type: BoatTypeEnum
    description: str
    brand: str
    fabrication_year: int
    photo_url: str
    license: LicenseEnum
    equipment: Optional[List[str]] = []  # Changed from Optional[str] to Optional[List[str]]
    caution: float
    nb_passenger: int
    nb_seat: int
    port: str
    latitude: float
    longitude: float
    motor: MotorEnum  # diesel, essence, aucun
    motor_power: int

# BoatCreate hérite de BoatBase sans demander explicitement l'owner_id
class BoatCreate(BoatBase):
    # owner_id sera injecté dans le endpoint à partir de current_user
    pass

class BoatGetter(GetterDict):
    def get(self, key, default=None):
        if key == "equipment":
            return self._obj.equipment_list  # renvoyer la liste issue du setter/getter
        return getattr(self._obj, key, default)

class BoatResponse(BoatBase):
    id: int
    owner_id: int

    @field_validator('equipment', mode='before')
    def validate_equipment(cls, v):
        """Convert string equipment to list if needed"""
        if isinstance(v, str):
            if not v:
                return []
            return [item.strip() for item in v.split(',') if item.strip()]
        return v or []

    class Config:
        orm_mode = True
        getter_dict = BoatGetter
        from_attributes = True

class BoatUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    fabrication_year: Optional[int] = None
    photo_url: Optional[str] = None
    license: Optional[LicenseEnum] = None
    boat_type: Optional[BoatTypeEnum] = None
    equipment: Optional[List[EquipmentEnum]] = None
    caution: Optional[float] = None
    nb_passenger: Optional[int] = None
    nb_seat: Optional[int] = None
    port: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    motor: Optional[MotorEnum] = None
    motor_power: Optional[int] = None

    class Config:
        from_attributes = True
