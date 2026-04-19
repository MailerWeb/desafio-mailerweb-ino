from __future__ import annotations

import logging
import time

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

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
        with SessionLocal() as db:
            pending_events = self._fetch_pending_events(db)

        logger.info(
            "Outbox worker fetched %s pending event(s): %s",
            len(pending_events),
            [event.id for event in pending_events],
        )
        return len(pending_events)

    def _pending_events_statement(self) -> Select[tuple[OutboxEvent]]:
        return (
            select(OutboxEvent)
            .where(
                OutboxEvent.status == OutboxEventStatus.PENDING,
                OutboxEvent.attempts < self.settings.outbox_max_attempts,
                or_(
                    OutboxEvent.next_retry_at.is_(None),
                    OutboxEvent.next_retry_at <= func.now(),
                ),
            )
            .order_by(OutboxEvent.created_at.asc(), OutboxEvent.id.asc())
            .limit(self.settings.worker_batch_size)
            .with_for_update(skip_locked=True)
        )

    def _fetch_pending_events(self, db: Session) -> list[OutboxEvent]:
        statement = self._pending_events_statement()
        return list(db.scalars(statement).all())
