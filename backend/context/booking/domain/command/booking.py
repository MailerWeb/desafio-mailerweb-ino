from uuid import UUID
from datetime import datetime
from typing import List, Optional
from libs.command import Command


class CreateBooking(Command):
    title: str
    room_id: UUID
    start_at: datetime
    end_at: datetime
    participants: List[str]
    created_by: UUID


class UpdateBooking(Command):
    id: UUID
    title: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    participants: Optional[List[str]] = None


class CancelBooking(Command):
    id: UUID


class GetBooking(Command):
    id: UUID


class ListBookings(Command):
    pass
