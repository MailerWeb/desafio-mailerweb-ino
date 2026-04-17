from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.room import Room


class RoomRepository(ABC):
    @abstractmethod
    async def get_by_id(self, room_id: UUID) -> Room | None: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Room | None: ...

    @abstractmethod
    async def list_all(self, active_only: bool = True) -> list[Room]: ...

    @abstractmethod
    async def create(
        self, name: str, capacity: int, location: str, description: str | None
    ) -> Room: ...

    @abstractmethod
    async def update(self, room_id: UUID, **kwargs) -> Room | None: ...

    @abstractmethod
    async def delete(self, room_id: UUID) -> bool: ...
