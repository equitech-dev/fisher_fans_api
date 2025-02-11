from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import ConfigDict

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reservation_date = Column(Date, nullable=False)
    nb_seats = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    # Relations
    trip = relationship("Trip", back_populates="reservations")
    user = relationship("User", back_populates="reservations")

    class Config:
        model_config = ConfigDict()