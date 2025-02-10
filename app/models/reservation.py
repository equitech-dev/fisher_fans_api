from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import ConfigDict

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    nb_places = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))

    user = relationship("User", back_populates="reservations")
    trip = relationship("Trip", back_populates="reservations")

    class Config:
        model_config = ConfigDict()