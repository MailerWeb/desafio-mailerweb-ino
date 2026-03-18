from pydantic import BaseModel, Field

from typing import Optional


class Room(BaseModel):
    name: str
    key: str | None = None
    capacity: int


class RoomCreate(BaseModel):
    name: str
    key: Optional[str] = None
    capacity: int = Field(gt=0, description="A capacidade deve ser maior que zero")


class RoomResponse(RoomCreate):
    id: int

    class Config:
        from_attributes = True
