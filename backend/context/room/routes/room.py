from typing import List
from uuid import UUID
from fastapi import APIRouter
from context.room.domain.entity.room import Room
from libs.output import OutputData
from libs.uow import UnitOfWork
from context.room.domain.command.room import CreateRoom, GetRoom, ListRooms
from context.room.domain.model.room import CreateRoomInput, RoomOutput
from context.room.services.room import create_room, get_room, list_rooms


route = APIRouter(tags=["rooms"], prefix="/rooms")


@route.post("/")
def create_new_room(data: CreateRoomInput) -> OutputData[RoomOutput]:
    """Create a new room."""
    uow = UnitOfWork()

    command = CreateRoom(
        name=data.name,
        capacity=data.capacity,
    )

    room = create_room(command=command, uow=uow)

    room_output = RoomOutput(
        id=room.id,
        name=room.name,
        capacity=room.capacity,
    )

    return OutputData(data=room_output)


@route.get("/")
def list_all_rooms() -> OutputData[List[RoomOutput]]:
    """List all rooms."""
    uow = UnitOfWork()

    command = ListRooms()

    rooms: List[Room] = list_rooms(command=command, uow=uow)

    rooms_output: List[RoomOutput] = [
        RoomOutput(id=r.id, name=r.name, capacity=r.capacity) for r in rooms
    ]

    return OutputData(data=rooms_output)


@route.get("/{room_id}")
def get_room_info(room_id: UUID) -> OutputData[RoomOutput]:
    """Get room details."""
    uow = UnitOfWork()

    command = GetRoom(id=room_id)

    room = get_room(command=command, uow=uow)

    room_output = RoomOutput(
        id=room.id,
        name=room.name,
        capacity=room.capacity,
    )

    return OutputData(data=room_output)