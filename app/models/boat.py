from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Boat(Base):
    __tablename__ = "boats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    boat_type = Column(String(50))
    motor = Column(String(50))
    capacity = Column(Integer)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="boats")
