from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    fish_name = Column(String(100), nullable=False)
    picture_url = Column(String(255))
    comment = Column(String(500))
    size = Column(Float)  # en cm
    weight = Column(Float)  # en kg
    location = Column(String(255))
    catch_date = Column(Date, nullable=False)
    released = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relation avec l'utilisateur
    user = relationship("User", back_populates="logs")