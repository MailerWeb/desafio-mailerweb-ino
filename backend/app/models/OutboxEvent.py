from pydantic import BaseModel

from datetime import datetime


class OutboxEvent(BaseModel):
    aggregate_type: str
    aggregate_id: int
    status: str
    payload: object
    retries: int = 0
    created_at: datetime
    process_at: datetime
