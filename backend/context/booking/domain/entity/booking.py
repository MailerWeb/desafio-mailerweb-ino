from dataclasses import dataclass, field
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum
from typing import List, Optional
from libs.entity import Entity


class BookingStatus(Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


@dataclass
class Booking(Entity):
    id: UUID
    title: str
    room_id: UUID
    start_at: datetime
    end_at: datetime
    status: BookingStatus
    created_by: UUID
    participants: List[str] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        title: str,
        room_id: UUID,
        start_at: datetime,
        end_at: datetime,
        participants: List[str],
        created_by: UUID,
    ) -> "Booking":
        if start_at >= end_at:
            raise ValueError("Start time must be before end time")
        duration = (end_at - start_at).total_seconds() / 60
        if duration < 15:
            raise ValueError("Minimum duration is 15 minutes")
        if duration > 480:  # 8 hours
            raise ValueError("Maximum duration is 8 hours")
        return cls(
            id=uuid4(),
            title=title,
            room_id=room_id,
            start_at=start_at,
            end_at=end_at,
            status=BookingStatus.ACTIVE,
            participants=participants,
            created_by=created_by,
        )

    def cancel(self):
        self.status = BookingStatus.CANCELLED

    def update(
        self,
        title: Optional[str] = None,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
        participants: Optional[List[str]] = None,
    ):
        if title:
            self.title = title
        if start_at:
            self.start_at = start_at
        if end_at:
            self.end_at = end_at
        if participants is not None:
            self.participants = participants
        # Re-validate
        if self.start_at >= self.end_at:
            raise ValueError("Start time must be before end time")
        duration = (self.end_at - self.start_at).total_seconds() / 60
        if duration < 15 or duration > 480:
            raise ValueError("Invalid duration")

    def __repr__(self) -> str:
        return f"Booking(id={self.id}, title={self.title}, room_id={self.room_id}, start_at={self.start_at}, end_at={self.end_at}, status={self.status.value})"