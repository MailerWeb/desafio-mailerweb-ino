"""Import ORM models here so Alembic autogenerate can discover them."""

from app.db.models.booking import Booking, BookingStatus
from app.db.models.booking_participant import BookingParticipant
from app.db.models.outbox_event import (
    OutboxEvent,
    OutboxEventStatus,
    OutboxEventType,
)
from app.db.models.room import Room
from app.db.models.user import User

__all__ = [
    "Booking",
    "BookingParticipant",
    "BookingStatus",
    "OutboxEvent",
    "OutboxEventStatus",
    "OutboxEventType",
    "Room",
    "User",
]
