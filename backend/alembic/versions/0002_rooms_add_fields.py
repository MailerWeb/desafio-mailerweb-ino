"""rooms: add location, description, is_active

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-17

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("rooms", sa.Column("location", sa.String(255), nullable=False, server_default=""))
    op.add_column("rooms", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("rooms", sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"))


def downgrade() -> None:
    op.drop_column("rooms", "is_active")
    op.drop_column("rooms", "description")
    op.drop_column("rooms", "location")
