from celery_app import celery_app
from libs.uow import UnitOfWork
from context.outbox.domain.command.outbox import ProcessOutboxEvents
from context.outbox.services.outbox import process_outbox_events


@celery_app.task
def process_outbox():
    """Task to process outbox events."""
    uow = UnitOfWork()
    command = ProcessOutboxEvents()
    process_outbox_events(command=command, uow=uow)