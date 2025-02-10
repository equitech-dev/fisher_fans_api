from datetime import date
from app.models.enum import TripTypeEnum, PricingTypeEnum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel, ConfigDict

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    practical_info = Column(Text)
    trip_type = Column(Enum(TripTypeEnum), nullable=False)
    pricing_type = Column(Enum(PricingTypeEnum), nullable=False)
    dates = Column(JSON)  # Liste des dates de début et fin
    schedules = Column(JSON)  # Liste des heures de départ et fin
    nb_passengers = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relations
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    boat_id = Column(Integer, ForeignKey("boats.id"), nullable=False)

    organizer = relationship("User", back_populates="trips")
    boat = relationship("Boat", back_populates="trips")
    reservations = relationship("Reservation", back_populates="trip")

    class Config:
        model_config = ConfigDict()