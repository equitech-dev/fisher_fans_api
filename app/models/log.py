from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fish_name = Column(String, nullable=False)
    size = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    date_caught = Column(DateTime, default=datetime.datetime.utcnow)
    released = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="logs")