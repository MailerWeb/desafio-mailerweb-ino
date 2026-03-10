import pytest
from context.room.domain.entity.room import Room
from context.room.errors.room import RoomNotFound

# Teste de criação de Room

def test_room_create():
    room = Room.create(
        name="Sala 1",
        capacity=10
    )
    assert room.name == "Sala 1"
    assert room.capacity == 10

# Teste de erro RoomNotFound

def test_room_not_found():
    with pytest.raises(RoomNotFound):
        raise RoomNotFound(detail="Room not found")
