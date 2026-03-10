from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from libs.output import OutputData
from libs.uow import UnitOfWork
from context.booking.domain.command.booking import CreateBooking, UpdateBooking, CancelBooking, GetBooking, ListBookings
from context.booking.domain.model.booking import CreateBookingInput, UpdateBookingInput, BookingOutput
from context.booking.services.booking import create_booking, update_booking, cancel_booking, get_booking, list_bookings
from context.booking.errors.booking import BookingNotFound, BookingOverlap, InvalidBookingTime
from context.room.errors.room import RoomNotFound
from libs.auth import get_current_user


route = APIRouter(tags=["bookings"], prefix="/bookings")


@route.post("/")
def create_new_booking(data: CreateBookingInput, current_user: UUID = Depends(get_current_user)) -> OutputData[BookingOutput]:
    """Create a new booking."""
    uow = UnitOfWork()

    command = CreateBooking(
        title=data.title,
        room_id=data.room_id,
        start_at=data.start_at,
        end_at=data.end_at,
        participants=data.participants,
        created_by=current_user,
    )

    try:
        booking = create_booking(command=command, uow=uow)
    except (BookingOverlap, InvalidBookingTime, RoomNotFound) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    booking_output = BookingOutput(
        id=booking.id,
        title=booking.title,
        room_id=booking.room_id,
        start_at=booking.start_at,
        end_at=booking.end_at,
        status=booking.status.value,
        participants=booking.participants,
        created_by=booking.created_by,
    )

    return OutputData(data=booking_output)


@route.put("/{booking_id}")
def update_existing_booking(booking_id: UUID, data: UpdateBookingInput, current_user: UUID = Depends(get_current_user)) -> OutputData[BookingOutput]:
    """Update a booking."""
    uow = UnitOfWork()

    command = UpdateBooking(
        id=booking_id,
        title=data.title,
        start_at=data.start_at,
        end_at=data.end_at,
        participants=data.participants,
    )

    try:
        booking = update_booking(command=command, uow=uow)
    except (BookingNotFound, BookingOverlap, InvalidBookingTime) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    booking_output = BookingOutput(
        id=booking.id,
        title=booking.title,
        room_id=booking.room_id,
        start_at=booking.start_at,
        end_at=booking.end_at,
        status=booking.status.value,
        participants=booking.participants,
        created_by=booking.created_by,
    )

    return OutputData(data=booking_output)


@route.delete("/{booking_id}")
def cancel_existing_booking(booking_id: UUID, current_user: UUID = Depends(get_current_user)) -> OutputData[dict]:
    """Cancel a booking."""
    uow = UnitOfWork()

    command = CancelBooking(id=booking_id)

    try:
        cancel_booking(command=command, uow=uow)
    except (BookingNotFound, InvalidBookingTime) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return OutputData(data={"message": "Booking cancelled"})


@route.get("/")
def list_all_bookings() -> OutputData[List[BookingOutput]]:
    """List all bookings."""
    uow = UnitOfWork()

    command = ListBookings()

    bookings = list_bookings(command=command, uow=uow)

    bookings_output = [
        BookingOutput(
            id=b.id,
            title=b.title,
            room_id=b.room_id,
            start_at=b.start_at,
            end_at=b.end_at,
            status=b.status.value,
            participants=b.participants,
            created_by=b.created_by,
        ) for b in bookings
    ]

    return OutputData(data=bookings_output)


@route.get("/{booking_id}")
def get_booking_info(booking_id: UUID) -> OutputData[BookingOutput]:
    """Get booking details."""
    uow = UnitOfWork()

    command = GetBooking(id=booking_id)

    try:
        booking = get_booking(command=command, uow=uow)
    except BookingNotFound as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    booking_output = BookingOutput(
        id=booking.id,
        title=booking.title,
        room_id=booking.room_id,
        start_at=booking.start_at,
        end_at=booking.end_at,
        status=booking.status.value,
        participants=booking.participants,
        created_by=booking.created_by,
    )

    return OutputData(data=booking_output)
