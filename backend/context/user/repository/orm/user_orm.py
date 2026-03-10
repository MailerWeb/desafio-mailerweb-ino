from uuid import uuid4
from sqlalchemy.types import Uuid, String
from sqlalchemy.schema import Column, Table

from context.user.domain.entity.user import User
from libs.database import REGISTRY

tabela_user = Table(
    "User",
    REGISTRY.metadata,
    Column("id", Uuid(as_uuid=True), default=uuid4, primary_key=True, index=True),
    Column("name", String(100), nullable=False, index=True, unique=True),
    Column("email", String(100), nullable=False, index=True, unique=True),
    Column("password", String(100), nullable=False),
)

user_orm_mapper = REGISTRY.map_imperatively(
    User, tabela_user, properties={"id": tabela_user.c.id}
)
