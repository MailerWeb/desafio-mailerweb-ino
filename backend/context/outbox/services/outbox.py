from typing import List

from libs.uow import UnitOfWorkAbstract
from context.outbox.repository.repo.outbox_repo import OutboxRepo
from context.outbox.domain.command.outbox import AddOutboxEvent, ProcessOutboxEvents, GetPendingEvents
from context.outbox.domain.entity.outbox import OutboxEvent
from libs.email import send_booking_notification


def add_outbox_event(command: AddOutboxEvent, uow: UnitOfWorkAbstract) -> OutboxEvent:
    """Add an event to the outbox."""
    event: OutboxEvent = OutboxEvent.create(
        event_type=command.event_type,
        event_data=command.event_data,
    )

    with uow:
        repo = OutboxRepo(uow.session)
        repo.add(event)
        uow.commit()

    return event


def get_pending_events(command: GetPendingEvents, uow: UnitOfWorkAbstract) -> List[OutboxEvent]:

    with uow:
        repo = OutboxRepo(uow.session)
        events: List[OutboxEvent] = repo.get_pending_events()

    return events


def process_outbox_events(command: ProcessOutboxEvents, uow: UnitOfWorkAbstract):

    with uow:
        repo = OutboxRepo(uow.session)
        events: List[OutboxEvent] = repo.get_pending_events(limit=10)

        for event in events:
            try:
                send_booking_notification(event.event_type.value, event.event_data)
                event.mark_processed()
            except Exception as e:
                print(f"Failed to process event {event.id}: {e}")
                event.mark_failed()

            repo.update_event(event)

        uow.commit()
