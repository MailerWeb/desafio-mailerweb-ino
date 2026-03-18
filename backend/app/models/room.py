from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.db import Base


class RoomDB(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    key = Column(String, nullable=True)
    capacity = Column(Integer, nullable=False)

    bookings = relationship("BookingDB", back_populates="room")
