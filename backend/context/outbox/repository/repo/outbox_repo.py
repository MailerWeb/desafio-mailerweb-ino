from abc import abstractmethod, ABC
from typing import List, Optional
from sqlalchemy.orm.session import Session

from context.outbox.domain.entity.outbox import OutboxEvent, OutboxStatus
from libs.repo import Repository


class OutboxRepoAbstrato(Repository, ABC):
    @abstractmethod
    def add(self, event: OutboxEvent) -> Optional[OutboxEvent]:
        pass

    @abstractmethod
    def get_pending_events(self, limit: int = 10) -> List[OutboxEvent]:
        pass

    @abstractmethod
    def update_event(self, event: OutboxEvent) -> Optional[OutboxEvent]:
        pass


class OutboxRepo(OutboxRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    def add(self, event: OutboxEvent) -> Optional[OutboxEvent]:
        self.session.add(event)
        return event

    def get_pending_events(self, limit: int = 10) -> List[OutboxEvent]:
        query = self.session.query(OutboxEvent)
        query = query.filter(
            OutboxEvent.status == OutboxStatus.PENDING
        )
        query = query.order_by(OutboxEvent.created_at)
        query = query.limit(limit)
        return query.all()

    def update_event(self, event: OutboxEvent) -> Optional[OutboxEvent]:
        self.session.merge(event)
        return event
