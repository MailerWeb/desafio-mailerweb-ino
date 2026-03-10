from uuid import UUID
from datetime import datetime
from libs.model import Model


class OutboxEventOutput(Model):
    id: UUID
    event_type: str
    event_data: dict
    status: str
    created_at: datetime
    processed_at: datetime = None
    retry_count: int