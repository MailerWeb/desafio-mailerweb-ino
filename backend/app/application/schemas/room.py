from uuid import UUID

from pydantic import BaseModel, Field


class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    capacity: int = Field(..., gt=0)
    location: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class RoomUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    capacity: int | None = Field(None, gt=0)
    location: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    is_active: bool | None = None


class RoomOut(BaseModel):
    id: UUID
    name: str
    capacity: int
    location: str
    description: str | None
    is_active: bool

    model_config = {"from_attributes": True}
