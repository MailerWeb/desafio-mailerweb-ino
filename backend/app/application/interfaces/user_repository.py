from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models import UserModel


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserModel | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserModel | None: ...

    @abstractmethod
    async def create(self, name: str, email: str, password_hash: str) -> UserModel: ...
