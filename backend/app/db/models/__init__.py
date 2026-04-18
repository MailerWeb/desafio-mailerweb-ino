"""Import ORM models here so Alembic autogenerate can discover them."""

from app.db.models.room import Room
from app.db.models.user import User

__all__ = ["Room", "User"]
