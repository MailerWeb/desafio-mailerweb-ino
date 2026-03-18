from pydantic import BaseModel, model_validator

from datetime import datetime, timedelta
from enum import Enum
from typing import List


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
    participants: List[str]

    @model_validator(mode="after")
    def validate_time(self) -> "BookingCreate":
        if self.start_at >= self.end_at:
            raise ValueError(
                "Horários de início e fim inválidos. O horário de início deve ser menor que o horário de fim."
            )
        elif (self.end_at - self.start_at) < timedelta(minutes=15) or (
            (self.end_at - self.start_at) > timedelta(hours=8)
        ):
            raise ValueError(
                "Tempo de duração deve ser maior ou igual a 15 min ou menor que 8 horas"
            )

        return self


class BookingResponse(BookingCreate):
    id: int

    class Config:
        from_attributes = True
