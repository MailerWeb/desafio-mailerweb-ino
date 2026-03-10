from typing import Final
from sqlalchemy.orm import registry
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm.session import Session, sessionmaker
from libs.env_manager import ENVS

REGISTRY: Final = registry()
metadata = MetaData()


def connect() -> Session:
    engine: Engine = create_engine(
        ENVS.DB_STRING_CONNECTION, isolation_level="AUTOCOMMIT"
    )
    _session: sessionmaker[Session] = sessionmaker(bind=engine, expire_on_commit=False)

    return _session()


def load_tables() -> None:

    # import modules which register mappers on import
    from context.booking.repository.orm import booking_orm  # noqa: F401
    from context.room.repository.orm import room_orm  # noqa: F401
    from context.outbox.repository.orm import outbox_orm  # noqa: F401
    from context.user.repository.orm import user_orm  # noqa: F401
    # additional contexts go here
    return