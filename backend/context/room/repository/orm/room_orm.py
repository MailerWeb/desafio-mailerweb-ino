from uuid import uuid4
from sqlalchemy.types import Uuid, String, Integer
from sqlalchemy.schema import Column, Table

from context.room.domain.entity.room import Room
from libs.database import REGISTRY

tabela_room = Table(
    "Room",
    REGISTRY.metadata,
    Column("id", Uuid(as_uuid=True), default=uuid4, primary_key=True, index=True),
    Column("name", String(100), nullable=False, index=True, unique=True),
    Column("capacity", Integer, nullable=False),
)

room_orm_mapper = REGISTRY.map_imperatively(
    Room, tabela_room, properties={"id": tabela_room.c.id}
)