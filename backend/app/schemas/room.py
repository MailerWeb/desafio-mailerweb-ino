from pydantic import BaseModel, Field


class Room(BaseModel):
    name: str
    key: str | None = None
    capacity: int = Field(gt=0, description="A capacidade deve ser maior que zero")


class RoomCreate(Room):
    pass


class RoomResponse(RoomCreate):
    id: int

    class Config:
        from_attributes = True
