from pydantic import BaseModel

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.db import Base


class User(BaseModel):
    name: str
    surname: str
    password: str
    email: str
    role: str


class UserInDB(User):
    hashed_password: str


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bookings = relationship("Booking", back_populates="user")
