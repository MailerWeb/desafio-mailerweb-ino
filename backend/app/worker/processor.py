from __future__ import annotations

import logging
import time

from sqlalchemy import func, or_, select

from app.core.config import get_settings
from app.db.enums import OutboxEventStatus
from app.db.models import OutboxEvent
from app.db.session import SessionLocal


logger = logging.getLogger(__name__)


class OutboxWorker:
    def __init__(self) -> None:
        self.settings = get_settings()

    def run_forever(self) -> None:
        logger.info(
            "Outbox worker started with poll interval %ss",
            self.settings.worker_poll_interval_seconds,
        )
        while True:
            processed = self.run_once()
            logger.debug("Outbox worker cycle completed. pending=%s", processed)
            time.sleep(self.settings.worker_poll_interval_seconds)

    def run_once(self) -> int:
        pending_events = self._count_pending_events()
        logger.info("Outbox worker found %s pending event(s)", pending_events)
        return pending_events

    def _count_pending_events(self) -> int:
        with SessionLocal() as db:
            statement = select(func.count(OutboxEvent.id)).where(
                OutboxEvent.status == OutboxEventStatus.PENDING,
                or_(
                    OutboxEvent.next_retry_at.is_(None),
                    OutboxEvent.next_retry_at <= func.now(),
                ),
            )
            count = db.scalar(statement)

        return int(count or 0)
