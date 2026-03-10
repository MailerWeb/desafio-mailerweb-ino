from abc import ABC
from typing import Any, Optional
from dataclasses import dataclass
from sqlalchemy.orm.session import Session
from sqlalchemy import text


@dataclass
class UnitOfWorkAbstract(ABC):
    session: Any

    def __enter__(self) -> Any:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def add(self, obj: Any):
        pass


@dataclass
class UnitOfWork(UnitOfWorkAbstract):
    schema: str = "public"
    session: Optional[Session] = None

    def __enter__(self) -> Any:
        from libs.database import connect

        if not self.session:
            self.session = connect()

        self.session.execute(text(f"SET search_path TO '{self.schema}'"))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def add(self, obj: Any):
        self.session.add(obj)