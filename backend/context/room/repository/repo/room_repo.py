from abc import abstractmethod, ABC
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm.session import Session

from context.room.domain.entity.room import Room
from libs.repo import Repository


class RoomRepoAbstrato(Repository, ABC):
    @abstractmethod
    def search_by_name(self, name: str) -> Optional[Room]:
        pass

    @abstractmethod
    def search_by_id(self, id: UUID) -> Optional[Room]:
        pass

    @abstractmethod
    def list(self) -> Optional[List[Room]]:
        pass

    @abstractmethod
    def add(self, room: Room) -> Optional[Room]:
        pass


class RoomRepo(RoomRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    def add(self, room: Room) -> Optional[Room]:
        self.session.add(room)
        return room

    def search_by_id(self, id: UUID) -> Optional[Room]:
        query = self.session.query(Room)
        query = query.filter(Room.id == id)
        room = query.first()
        return room

    def search_by_name(self, name: str) -> Optional[Room]:
        query = self.session.query(Room)
        query = query.filter(Room.name == name)
        room = query.first()
        return room

    def list(self) -> Optional[List[Room]]:
        consulta = self.session.query(Room)
        rooms = consulta.all()
        return rooms