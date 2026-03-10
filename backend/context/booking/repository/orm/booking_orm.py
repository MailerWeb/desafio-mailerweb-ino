from uuid import uuid4
from sqlalchemy.types import Uuid, String, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.schema import Column, Table

from context.booking.domain.entity.booking import Booking, BookingStatus
from libs.database import REGISTRY

tabela_booking = Table(
    "Booking",
    REGISTRY.metadata,
    Column("id", Uuid(as_uuid=True), default=uuid4, primary_key=True, index=True),
    Column("title", String(200), nullable=False),
    Column("room_id", Uuid(as_uuid=True), nullable=False, index=True),
    Column("start_at", DateTime(timezone=True), nullable=False, index=True),
    Column("end_at", DateTime(timezone=True), nullable=False, index=True),
    Column("status", SQLEnum(BookingStatus), nullable=False, default=BookingStatus.ACTIVE),
    Column("participants", JSON, nullable=False, default=list),
    Column("created_by", Uuid(as_uuid=True), nullable=False),
)

booking_orm_mapper = REGISTRY.map_imperatively(
    Booking, tabela_booking, properties={"id": tabela_booking.c.id}
)
