import pytest
from uuid import uuid4
from context.outbox.domain.entity.outbox import OutboxEvent, OutboxEventType

# Teste de criação de evento outbox

def test_outbox_event_create():
    event = OutboxEvent(
        id=uuid4(),
        event_type=OutboxEventType.BOOKING_CREATED,
        event_data={"booking_id": "uuid-booking"}
    )
    assert event.event_type == OutboxEventType.BOOKING_CREATED
    assert event.event_data["booking_id"] == "uuid-booking"
