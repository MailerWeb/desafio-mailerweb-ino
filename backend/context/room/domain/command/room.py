from uuid import UUID
from libs.command import Command


class CreateRoom(Command):
    name: str
    capacity: int


class GetRoom(Command):
    id: UUID


class ListRooms(Command):
    pass