from pydantic import BaseModel


class Room(BaseModel):
    name: str
    key: str | None = None
    capacity: int
