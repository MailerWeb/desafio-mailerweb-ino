from fastapi import APIRouter
from libs.output import OutputData
from libs.uow import UnitOfWork
from context.outbox.domain.command.outbox import ProcessOutboxEvents, GetPendingEvents
from context.outbox.services.outbox import process_outbox_events, get_pending_events


route = APIRouter(tags=["outbox"], prefix="/outbox")


@route.post("/process")
def process_events():
    """Process pending outbox events."""
    uow = UnitOfWork()

    command = ProcessOutboxEvents()

    process_outbox_events(command=command, uow=uow)

    return OutputData(data={"message": "Events processed"})


@route.get("/pending")
def get_pending():
    """Get pending events."""
    uow = UnitOfWork()

    command = GetPendingEvents()

    events = get_pending_events(command=command, uow=uow)

    return OutputData(data=[{"id": e.id, "type": e.event_type.value, "data": e.event_data} for e in events])