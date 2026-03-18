from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import timezone
from app.db.db import Base


class OutboxEventDB(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True, index=True)
    aggregate_type = Column(String, nullable=False)
    aggregate_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, default="PENDING")
    retries = Column(Integer, default=0)
    created_at = Column(DateTime, default=timezone.utc)
    processed_at = Column(DateTime, nullable=True)
