from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..schemas import BookingCreate, BookingStatus
from ..models import BookingDB, OutboxEventDB


def check_overlap(db: Session, booking_data: BookingCreate, user_id: int):
    conflict = (
        db.query(BookingDB)
        .with_for_update()
        .filter(
            BookingDB.room_id == booking_data.room_id,
            BookingDB.status == BookingStatus.ACTIVE,
            booking_data.start_at < BookingDB.end_at,
            booking_data.end_at > BookingDB.start_at,
        )
    ).first()

    if conflict:
        raise HTTPException(status_code=400, detail="Conflito de horários!")
    else:
        return create_booking(db, booking_data, user_id)


def create_booking(db: Session, booking_data: BookingCreate, user_id: int):
    try:
        new_booking = BookingDB(**booking_data.model_dump(), user_id=user_id)
        db.add(new_booking)
        db.flush()

        event = OutboxEventDB(
            aggregate_type="BOOKING",
            aggregate_id=new_booking.id,
            event_type="BOOKING_CREATE",
            payload={
                "title": new_booking.title,
                "room_id": new_booking.room_id,
                "start": new_booking.start_at.isoformat(),
                "end": new_booking.end_at.isoformat(),
                "participants": booking_data.participants,
            },
        )

        db.add(event)
        db.commit()
        db.refresh(new_booking)
        return new_booking
    except SQLAlchemyError as e:
        db.rollback()
        raise e
