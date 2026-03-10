from abc import abstractmethod, ABC
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm.session import Session

from context.user.domain.entity.user import User
from libs.repo import Repository


class UserRepoAbstrato(Repository, ABC):
    @abstractmethod
    def search_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def search_by_id(self, id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def list(self) -> Optional[List[User]]:
        pass

    @abstractmethod
    def add(self, user: User) -> Optional[User]:
        pass

    @abstractmethod
    def put(self, entity: User) -> Optional[User]:
        pass


class UserRepo(UserRepoAbstrato):
    def __init__(self, session: Session):
        self.session = session

    # POST
    def add(self, user: User) -> Optional[User]:
        self.session.add(user)
        return user

    # GET ONE
    def search_by_id(self, id: UUID) -> Optional[User]:
        query = self.session.query(User)
        query = query.filter(User.id == id)
        user = query.first()
        return user

    def search_by_email(self, email: str) -> Optional[User]:
        query = self.session.query(User)
        query = query.filter(User.email == email)
        user = query.first()
        return user

    # GET ALL
    def list(self) -> Optional[List[User]]:
        consulta = self.session.query(User)
        users = consulta.all()
        return users

    # PUT
    def put(self, entity: User) -> Optional[User]:
        self.session.merge(entity)
        return entity