from app.models.enum import MotorEnum, LicenseEnum, BoatTypeEnum, EquipmentEnum
from sqlalchemy import Column, Integer, String, Text, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import ConfigDict

class Boat(Base):
    __tablename__ = "boats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    brand = Column(String(100))
    fabrication_year = Column(Integer)
    photo_url = Column(String(100))
    nb_passenger = Column(Integer)
    nb_seat = Column(Integer)
    port = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    motor_power = Column(Integer)
    motor = Column(Enum(MotorEnum))
    license = Column(Enum(LicenseEnum))
    boat_type = Column(Enum(BoatTypeEnum))
    equipment = Column(String(250))  # Store as comma-separated values
    caution = Column(Float)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="boats")
    trips = relationship("Trip", back_populates="boat")

    @property
    def equipment_list(self):
        return self.equipment.split(',') if self.equipment else []

    @equipment_list.setter
    def equipment_list(self, value):
        self.equipment = ','.join(value)

    class Config:
        model_config = ConfigDict()