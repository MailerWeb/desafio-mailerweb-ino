from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum
from libs.entity import Entity


class OutboxEventType(Enum):
    BOOKING_CREATED = "BOOKING_CREATED"
    BOOKING_UPDATED = "BOOKING_UPDATED"
    BOOKING_CANCELED = "BOOKING_CANCELED"


class OutboxStatus(Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"


@dataclass
class OutboxEvent(Entity):
    id: UUID
    event_type: OutboxEventType
    event_data: dict
    status: OutboxStatus = OutboxStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    processed_at: datetime = None
    retry_count: int = 0

    @classmethod
    def create(cls, event_type: OutboxEventType, event_data: dict) -> "OutboxEvent":
        return cls(
            id=uuid4(),
            event_type=event_type,
            event_data=event_data,
        )

    def mark_processed(self):
        self.status = OutboxStatus.PROCESSED
        self.processed_at = datetime.utcnow()

    def mark_failed(self):
        self.status = OutboxStatus.FAILED
        self.retry_count += 1

    def __repr__(self) -> str:
        return f"OutboxEvent(id={self.id}, event_type={self.event_type.value}, status={self.status.value})"