from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import ConfigDict

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    fish = Column(String(100))
    picture = Column(String(255))
    comment = Column(Text)
    size = Column(Float)
    weight = Column(Float)
    place = Column(String(100))
    kept = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="logs")

    class Config:
        model_config = ConfigDict()