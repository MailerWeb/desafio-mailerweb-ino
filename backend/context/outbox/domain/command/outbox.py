from libs.command import Command
from context.outbox.domain.entity.outbox import OutboxEventType


class AddOutboxEvent(Command):
    event_type: OutboxEventType
    event_data: dict


class ProcessOutboxEvents(Command):
    pass


class GetPendingEvents(Command):
    pass