from pydantic import BaseModel

from datetime import datetime


class Booking(BaseModel):
    title: str
    room: int
    user: int
    start: datetime
    end: datetime
    status: str
