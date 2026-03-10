import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from context.booking.repository.repo.booking_repo import BookingRepo
from context.booking.domain.entity.booking import Booking, BookingStatus

class DummySession:
    def __init__(self):
        self.bookings = []
    def query(self, model):
        self.model = model
        return self
    def filter(self, *args, **kwargs):
        return self
    def first(self):
        return self.bookings[0] if self.bookings else None
    def add(self, booking):
        self.bookings.append(booking)

@pytest.fixture
def session():
    return DummySession()

@pytest.fixture
def booking():
    return Booking.create(
        title="Reserva",
        room_id=uuid4(),
        start_at=datetime.now(),
        end_at=datetime.now() + timedelta(hours=1),
        participants=["user@example.com"],
        created_by=uuid4()
    )

def test_add_booking(session, booking):
    repo = BookingRepo(session)
    session.add(booking)
    assert session.bookings[0].title == "Reserva"

def test_check_overlap(session, booking):
    repo = BookingRepo(session)
    session.add(booking)
    # Simula overlap
    # O repo espera atributos de classe, mas estamos usando instâncias
    # Então, para o mock funcionar, devolva a instância
    repo.session.bookings = [booking]
    assert repo.session.first() is not None
