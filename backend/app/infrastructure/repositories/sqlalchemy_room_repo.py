from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.room_repository import RoomRepository
from app.domain.entities.room import Room
from app.infrastructure.database.models import RoomModel


def _to_entity(model: RoomModel) -> Room:
    return Room(
        id=model.id,
        name=model.name,
        capacity=model.capacity,
        location=model.location,
        description=model.description,
        is_active=model.is_active,
        created_at=model.created_at,
    )


class SQLAlchemyRoomRepository(RoomRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, room_id: UUID) -> Room | None:
        result = await self.session.execute(
            select(RoomModel).where(RoomModel.id == room_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_name(self, name: str) -> Room | None:
        result = await self.session.execute(
            select(RoomModel).where(RoomModel.name == name)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_all(self, active_only: bool = True) -> list[Room]:
        query = select(RoomModel)
        if active_only:
            query = query.where(RoomModel.is_active.is_(True))
        query = query.order_by(RoomModel.name)
        result = await self.session.execute(query)
        return [_to_entity(m) for m in result.scalars().all()]

    async def create(
        self,
        name: str,
        capacity: int,
        location: str,
        description: str | None,
    ) -> Room:
        model = RoomModel(
            name=name,
            capacity=capacity,
            location=location,
            description=description,
        )
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return _to_entity(model)

    async def update(self, room_id: UUID, **kwargs) -> Room | None:
        result = await self.session.execute(
            select(RoomModel).where(RoomModel.id == room_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        await self.session.flush()
        await self.session.refresh(model)
        return _to_entity(model)

    async def delete(self, room_id: UUID) -> bool:
        result = await self.session.execute(
            select(RoomModel).where(RoomModel.id == room_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        model.is_active = False
        await self.session.flush()
        return True
