from pydantic import BaseModel

from datetime import datetime
from enum import Enum
from typing import Optional


class OutboxStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class OutboxEvent(BaseModel):
    aggregate_type: str
    aggregate_id: int
    status: str
    payload: object
    retries: int = 0
    created_at: datetime
    process_at: datetime


class OutboxEventResponse(BaseModel):
    id: int
    aggregate_type: str
    aggregate_id: int
    event_type: str
    status: OutboxStatus
    payload: dict
    retries: int
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
