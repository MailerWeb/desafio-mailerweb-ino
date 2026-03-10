import pytest
from uuid import uuid4
from datetime import datetime
from context.booking.domain.entity.booking import Booking



def test_booking_create():
    booking = Booking.create(
        title="Reunião",
        room_id=uuid4(),
        start_at=datetime.fromisoformat("2026-03-10T10:00:00"),
        end_at=datetime.fromisoformat("2026-03-10T11:00:00"),
        participants=["user@example.com"],
        created_by=uuid4()
    )
    assert booking.title == "Reunião"
    assert booking.status.name == "ACTIVE"



def test_booking_invalid_time():
    with pytest.raises(ValueError):
        Booking.create(
            title="Reunião",
            room_id=uuid4(),
            start_at=datetime.fromisoformat("2026-03-10T12:00:00"),
            end_at=datetime.fromisoformat("2026-03-10T11:00:00"),
            participants=["user@example.com"],
            created_by=uuid4()
        )
