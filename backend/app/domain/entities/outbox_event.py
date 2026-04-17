import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


class EventType(enum.Enum):
    BOOKING_CREATED = "BOOKING_CREATED"
    BOOKING_UPDATED = "BOOKING_UPDATED"
    BOOKING_CANCELED = "BOOKING_CANCELED"


class OutboxStatus(enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"


@dataclass
class OutboxEvent:
    event_type: EventType
    booking_id: UUID
    payload: dict[str, Any]
    id: UUID = field(default_factory=uuid4)
    idempotency_key: UUID = field(default_factory=uuid4)
    status: OutboxStatus = OutboxStatus.PENDING
    attempts: int = 0
    max_attempts: int = 5
    processed_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def can_retry(self) -> bool:
        return (
            self.status != OutboxStatus.PROCESSED and self.attempts < self.max_attempts
        )

    def mark_processed(self) -> None:
        self.status = OutboxStatus.PROCESSED
        self.processed_at = datetime.now(timezone.utc)

    def mark_failed(self) -> None:
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.status = OutboxStatus.FAILED
