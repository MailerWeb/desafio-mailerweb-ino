import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from context.booking.services.booking import create_booking
from context.booking.domain.command.booking import CreateBooking
from context.booking.errors.booking import BookingOverlap

class DummySession:
    def __init__(self):
        self.rooms = []
        self.bookings = []
        self.last_filter_id = None
    def query(self, model):
        self.model = model
        return self
    def filter(self, expr):
        # expr is Room.id == id or Room.name == name
        if hasattr(expr, 'right') and hasattr(expr, 'left'):
            if expr.left.name == 'id':
                self.last_filter_id = expr.right.value
            elif expr.left.name == 'name':
                self.last_filter_name = expr.right.value
        return self
    def first(self):
        if self.model.__name__ == "Room":
            for room in self.rooms:
                if hasattr(self, 'last_filter_id') and getattr(room, 'id', None) == self.last_filter_id:
                    return room
                if hasattr(self, 'last_filter_name') and getattr(room, 'name', None) == self.last_filter_name:
                    return room
            return None
        if self.model.__name__ == "Booking":
            return self.bookings[0] if self.bookings else None
        return None
    def add(self, obj):
        if obj.__class__.__name__ == "Room":
            self.rooms.append(obj)
        elif obj.__class__.__name__ == "Booking":
            self.bookings.append(obj)
    def all(self):
        if self.model.__name__ == "Room":
            return self.rooms
        return []

class DummyUow:
    def __init__(self):
        self.session = DummySession()
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass
    def commit(self): pass

@pytest.fixture
def uow():
    return DummyUow()

@pytest.fixture
def booking_command():
    return CreateBooking(
        title="Reunião",
        room_id=uuid4(),
        start_at=datetime.now(),
        end_at=datetime.now() + timedelta(hours=1),
        participants=["user@example.com"],
        created_by=uuid4()
    )
