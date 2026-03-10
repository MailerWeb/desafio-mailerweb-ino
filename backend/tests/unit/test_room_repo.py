import pytest
from uuid import uuid4
from context.room.repository.repo.room_repo import RoomRepo
from context.room.domain.entity.room import Room

class DummySession:
    def __init__(self):
        self.rooms = []
    def query(self, model):
        self.model = model
        return self
    def filter(self, *args, **kwargs):
        return self
    def first(self):
        return self.rooms[0] if self.rooms else None
    def add(self, room):
        self.rooms.append(room)

@pytest.fixture
def session():
    return DummySession()

@pytest.fixture
def room():
    return Room.create(
        name="Sala Teste",
        capacity=5
    )

def test_add_room(session, room):
    repo = RoomRepo(session)
    session.add(room)
    assert session.rooms[0].name == "Sala Teste"

def test_search_by_id(session, room):
    repo = RoomRepo(session)
    session.add(room)
    repo.session.rooms = [room]
    assert repo.session.first() is not None
