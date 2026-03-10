from datetime import datetime
from typing import List, Optional
from libs.uow import UnitOfWorkAbstract

from context.booking.repository.repo.booking_repo import BookingRepo
from context.booking.domain.command.booking import CreateBooking, UpdateBooking, CancelBooking, GetBooking, ListBookings
from context.booking.domain.entity.booking import Booking, BookingStatus
from context.booking.errors.booking import BookingNotFound, BookingOverlap, InvalidBookingTime
from context.room.repository.repo.room_repo import RoomRepo
from context.room.errors.room import RoomNotFound
from context.outbox.domain.command.outbox import AddOutboxEvent
from context.outbox.domain.entity.outbox import OutboxEventType
from context.outbox.services.outbox import add_outbox_event


def create_booking(command: CreateBooking, uow: UnitOfWorkAbstract) -> Booking:

    # Validate room exists
    with uow:
        room_repo = RoomRepo(uow.session)
        room = room_repo.search_by_id(command.room_id)
        if not room:
            raise RoomNotFound(detail="Room not found", status_code=404)

        booking_repo = BookingRepo(uow.session)

        # Check overlap
        if booking_repo.check_overlap(command.room_id, command.start_at, command.end_at):
            raise BookingOverlap(detail="Booking overlaps with existing booking", status_code=409)

        booking = Booking.create(
            title=command.title,
            room_id=command.room_id,
            start_at=command.start_at,
            end_at=command.end_at,
            participants=command.participants,
            created_by=command.created_by,
        )

        booking_repo.add(booking)

        # Add to outbox
        event_data = {
            "booking_id": str(booking.id),
            "title": booking.title,
            "room_id": str(booking.room_id),
            "start_at": booking.start_at.isoformat(),
            "end_at": booking.end_at.isoformat(),
            "participants": booking.participants,
        }
        outbox_command = AddOutboxEvent(event_type=OutboxEventType.BOOKING_CREATED, event_data=event_data)
        add_outbox_event(outbox_command, uow)

        uow.commit()

    return booking


def update_booking(command: UpdateBooking, uow: UnitOfWorkAbstract) -> Booking:
    with uow:
        booking_repo = BookingRepo(uow.session)
        booking: Optional[Booking] = booking_repo.search_by_id(command.id)

        if not booking:
            raise BookingNotFound(detail="Booking not found", status_code=404)

        if booking.status == BookingStatus.CANCELLED:
            raise InvalidBookingTime(detail="Cannot update cancelled booking", status_code=400)

        # Check overlap if times changed
        new_start: datetime = command.start_at or booking.start_at
        new_end: datetime = command.end_at or booking.end_at
        if booking_repo.check_overlap(booking.room_id, new_start, new_end, exclude_id=booking.id):
            raise BookingOverlap(detail="Updated booking overlaps with existing booking", status_code=409)

        booking.update(
            title=command.title,
            start_at=command.start_at,
            end_at=command.end_at,
            participants=command.participants,
        )

        booking_repo.put(booking)

        # Add to outbox
        event_data = {
            "booking_id": str(booking.id),
            "title": booking.title,
            "room_id": str(booking.room_id),
            "start_at": booking.start_at.isoformat(),
            "end_at": booking.end_at.isoformat(),
            "participants": booking.participants,
        }
        outbox_command = AddOutboxEvent(event_type=OutboxEventType.BOOKING_UPDATED, event_data=event_data)
        add_outbox_event(outbox_command, uow)

        uow.commit()

    return booking


def cancel_booking(command: CancelBooking, uow: UnitOfWorkAbstract) -> Booking:
    with uow:
        booking_repo = BookingRepo(uow.session)
        booking: Optional[Booking] = booking_repo.search_by_id(command.id)

        if not booking:
            raise BookingNotFound(detail="Booking not found", status_code=404)

        if booking.status == BookingStatus.CANCELLED:
            raise InvalidBookingTime(detail="Booking already cancelled", status_code=400)

        booking.cancel()
        booking_repo.put(booking)

        # Add to outbox
        event_data = {
            "booking_id": str(booking.id),
            "title": booking.title,
            "room_id": str(booking.room_id),
            "start_at": booking.start_at.isoformat(),
            "end_at": booking.end_at.isoformat(),
            "participants": booking.participants,
        }
        outbox_command = AddOutboxEvent(event_type=OutboxEventType.BOOKING_CANCELED, event_data=event_data)
        add_outbox_event(outbox_command, uow)

        uow.commit()

    return booking


def get_booking(command: GetBooking, uow: UnitOfWorkAbstract) -> Booking:
    """Get a booking by ID."""
    with uow:
        booking_repo = BookingRepo(uow.session)
        booking: Optional[Booking] = booking_repo.search_by_id(command.id)

        if not booking:
            raise BookingNotFound(detail="Booking not found", status_code=404)

    return booking


def list_bookings(command: ListBookings, uow: UnitOfWorkAbstract) -> List[Booking]:
    """List all bookings."""
    with uow:
        booking_repo = BookingRepo(uow.session)
        bookings = booking_repo.list()

    return bookings or []