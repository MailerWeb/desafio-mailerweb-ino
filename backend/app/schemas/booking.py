from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta
from typing import List


class BookingBase(BaseModel):
    title: str
    room_id: int
    start_at: datetime
    end_at: datetime
    participants: List[str]


class BookingCreate(BookingBase):
    @field_validator("start_at", "end_at")
    @classmethod
    def check_timezone(cls, v: datetime):
        if v.tzinfo is None:
            raise ValueError("As datas devem conter Timezone (ISO 8601)")
        return v

    @field_validator("end_at")
    @classmethod
    def validate_duration(cls, v: datetime, info):
        start = info.data.get("start_at")
        if not start:
            return v

        duration = v - start
        if duration < timedelta(minutes=15):
            raise ValueError("A duração mínima é de 15 minutos.")
        if duration > timedelta(hours=8):
            raise ValueError("A duração máxima é de 8 horas.")
        return v


class BookingResponse(BookingBase):
    id: int
    status: str
    user_id: int

    class Config:
        from_attributes = True
