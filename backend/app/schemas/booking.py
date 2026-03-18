from pydantic import BaseModel

from datetime import datetime
from enum import Enum


class BookingStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"


class Booking(BaseModel):
    title: str
    room: int
    user: int
    start: datetime
    end: datetime
    status: str


class BookingCreate(BaseModel):
    title: str
    room_id: int
    user_id: int
    start_at: datetime
    end_at: datetime
    status: BookingStatus = BookingStatus.ACTIVE


class BookingResponse(BookingCreate):
    id: int

    class Config:
        from_attributes = True
