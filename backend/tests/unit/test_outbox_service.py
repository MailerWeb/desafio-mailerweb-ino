import pytest
from uuid import uuid4
from context.outbox.services.outbox import add_outbox_event
from context.outbox.domain.command.outbox import AddOutboxEvent
from context.outbox.domain.entity.outbox import OutboxEventType

class DummyUow:
    def __init__(self):
        self.events = []
        self.session = self
    def add(self, event):
        self.events.append(event)
    def commit(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.fixture
def uow():
    return DummyUow()

def test_add_outbox_event(uow):
    command = AddOutboxEvent(
        event_type=OutboxEventType.BOOKING_CREATED,
        event_data={"booking_id": str(uuid4())}
    )
    add_outbox_event(command, uow)
    assert uow.events
