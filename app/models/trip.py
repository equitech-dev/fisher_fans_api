from datetime import date
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    trip_date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    boat_id = Column(Integer, ForeignKey('boats.id'), nullable=False)
    organizer_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    boat = relationship('Boat', back_populates='trips')
    organizer = relationship('User', back_populates='trips')

    def __init__(self, title, trip_date, price, boat, organizer):
        self.title = title
        self.trip_date = trip_date
        self.price = price
        self.boat = boat
        self.organizer = organizer