from uuid import UUID
from datetime import datetime
from pydantic import Field, EmailStr
from typing import List, Optional
from libs.model import Model


class CreateBookingInput(Model):
    title: str = Field(..., min_length=1)
    room_id: UUID
    start_at: datetime
    end_at: datetime
    participants: List[EmailStr] = Field(default_factory=list)


class UpdateBookingInput(Model):
    title: Optional[str] = Field(None, min_length=1)
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    participants: Optional[List[EmailStr]] = None


class BookingOutput(Model):
    id: UUID
    title: str
    room_id: UUID
    start_at: datetime
    end_at: datetime
    status: str
    participants: List[str]
    created_by: UUID