from uuid import UUID
from pydantic import Field
from libs.model import Model


class CreateRoomInput(Model):
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)


class RoomOutput(Model):
    id: UUID
    name: str
    capacity: int