from typing import List, Optional

from libs.uow import UnitOfWorkAbstract
from context.room.repository.repo.room_repo import RoomRepo
from context.room.domain.command.room import CreateRoom, GetRoom, ListRooms
from context.room.domain.entity.room import Room
from context.room.errors.room import RoomNotFound, RoomNameExists


def create_room(command: CreateRoom, uow: UnitOfWorkAbstract) -> Room:
    """Create a new room."""
    room = Room.create(
        name=command.name,
        capacity=command.capacity,
    )

    with uow:
        repo = RoomRepo(uow.session)

        name_exists = repo.search_by_name(room.name)

        if name_exists:
            raise RoomNameExists(detail="Room name already exists", status_code=400)

        repo.add(room)
        uow.commit()

    return room


def get_room(command: GetRoom, uow: UnitOfWorkAbstract) -> Room:
    """Get a room by ID."""
    with uow:
        repo = RoomRepo(uow.session)
        room: Optional[Room] = repo.search_by_id(command.id)

        if not room:
            raise RoomNotFound(detail="Room not found", status_code=404)

    return room


def list_rooms(command: ListRooms, uow: UnitOfWorkAbstract) -> List[Room]:
    """List all rooms."""
    with uow:
        repo = RoomRepo(uow.session)
        rooms = repo.list()

    return rooms or []