from dataclasses import dataclass
from uuid import uuid4, UUID
from libs.entity import Entity


@dataclass
class Room(Entity):
    id: UUID
    name: str
    capacity: int

    @classmethod
    def create(cls, name: str, capacity: int) -> "Room":
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        return cls(
            id=uuid4(),
            name=name,
            capacity=capacity,
        )

    def __repr__(self) -> str:
        return f"Room(id={self.id}, name={self.name}, capacity={self.capacity})"