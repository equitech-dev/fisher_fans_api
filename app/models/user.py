from sqlalchemy import Column, Integer, String, Enum, BigInteger
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enum import StatusEnum
from pydantic import ConfigDict

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    firstname = Column(String(100))
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    picture = Column(String(255))
    boat_license = Column(BigInteger)
    insurance = Column(String(255))
    company_name = Column(String(255))
    siret = Column(String(14))
    rcs = Column(String(14))
    status = Column(Enum(StatusEnum), nullable=False)
    role = Column(String(50), nullable=False, default="user")

    boats = relationship("Boat", back_populates="owner", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="organizer", cascade="all, delete-orphan")

    class Config:
        model_config = ConfigDict()
