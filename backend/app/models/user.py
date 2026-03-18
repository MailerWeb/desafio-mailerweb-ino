from pydantic import BaseModel

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.db import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bookings = relationship("BookingDB", back_populates="user")
