from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.room_repository import RoomRepository
from app.application.schemas.room import RoomCreate, RoomOut, RoomUpdate
from app.domain.entities.room import Room
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.sqlalchemy_room_repo import (
    SQLAlchemyRoomRepository,
)


def _to_out(room: Room) -> RoomOut:
    return RoomOut(
        id=room.id,
        name=room.name,
        capacity=room.capacity,
        location=room.location,
        description=room.description,
        is_active=room.is_active,
    )


class RoomService:
    def __init__(self, session: AsyncSession):
        self.repo: RoomRepository = SQLAlchemyRoomRepository(session)

    async def create(self, data: RoomCreate) -> RoomOut:
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=409, detail="Já existe uma sala com esse nome."
            )

        room = await self.repo.create(
            name=data.name,
            capacity=data.capacity,
            location=data.location,
            description=data.description,
        )
        return _to_out(room)

    async def get(self, room_id: UUID) -> RoomOut:
        room = await self.repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Sala não encontrada.")
        return _to_out(room)

    async def list_all(self, active_only: bool = True) -> list[RoomOut]:
        rooms = await self.repo.list_all(active_only=active_only)
        return [_to_out(r) for r in rooms]

    async def update(self, room_id: UUID, data: RoomUpdate) -> RoomOut:
        if data.name:
            existing = await self.repo.get_by_name(data.name)
            if existing and existing.id != room_id:
                raise HTTPException(
                    status_code=409, detail="Já existe uma sala com esse nome."
                )

        room = await self.repo.update(room_id, **data.model_dump(exclude_none=True))
        if not room:
            raise HTTPException(status_code=404, detail="Sala não encontrada.")
        return _to_out(room)

    async def delete(self, room_id: UUID) -> None:
        deleted = await self.repo.delete(room_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Sala não encontrada.")


async def get_room_service(session: AsyncSession = Depends(get_db)) -> RoomService:
    return RoomService(session)


RoomServiceDep = Annotated[RoomService, Depends(get_room_service)]
