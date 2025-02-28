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
    equipment = Column(String(255))  # Stocké comme chaîne, converti en liste lors de la sérialisation
    caution = Column(Float)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="boats")
    trips = relationship("Trip", back_populates="boat")

    @property
    def equipment_list(self):
        """Convert equipment string to list, handling empty values"""
        if not self.equipment or self.equipment.strip() == "":
            return []
        return [item.strip() for item in self.equipment.split(',') if item.strip()]

    @equipment_list.setter
    def equipment_list(self, value):
        """Store list as comma-separated string, handling empty lists"""
        if not value:
            self.equipment = ""
        else:
            self.equipment = ','.join(filter(None, value))

    def get_equipment_list(self):
        """Legacy method for compatibility"""
        return self.equipment_list

    class Config:
        model_config = ConfigDict()