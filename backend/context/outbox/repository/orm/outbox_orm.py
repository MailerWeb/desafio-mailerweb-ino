from uuid import uuid4
from sqlalchemy.types import Uuid, Enum as SQLEnum, JSON, DateTime, Integer
from sqlalchemy.schema import Column, Table
from datetime import datetime

from context.outbox.domain.entity.outbox import OutboxEvent, OutboxEventType, OutboxStatus
from libs.database import REGISTRY

tabela_outbox = Table(
    "OutboxEvent",
    REGISTRY.metadata,
    Column("id", Uuid(as_uuid=True), default=uuid4, primary_key=True, index=True),
    Column("event_type", SQLEnum(OutboxEventType), nullable=False),
    Column("event_data", JSON, nullable=False),
    Column("status", SQLEnum(OutboxStatus), nullable=False, default=OutboxStatus.PENDING),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow),
    Column("processed_at", DateTime, nullable=True),
    Column("retry_count", Integer, nullable=False, default=0),
)

outbox_orm_mapper = REGISTRY.map_imperatively(
    OutboxEvent, tabela_outbox, properties={"id": tabela_outbox.c.id}
)