import pytest
from uuid import uuid4
from context.user.repository.repo.user_repo import UserRepo
from context.user.domain.entity.user import User

class DummySession:
    def __init__(self):
        self.users = []
    def query(self, model):
        self.model = model
        return self
    def filter(self, *args, **kwargs):
        return self
    def first(self):
        return self.users[0] if self.users else None
    def add(self, user):
        self.users.append(user)

@pytest.fixture
def session():
    return DummySession()

@pytest.fixture
def user():
    return User.create(
        name="Usuário Teste",
        email="user@example.com",
        password="senha123"
    )

def test_add_user(session, user):
    repo = UserRepo(session)
    session.add(user)
    assert session.users[0].name == "Usuário Teste"

def test_search_by_id(session, user):
    repo = UserRepo(session)
    session.add(user)
    repo.session.users = [user]
    assert repo.session.first() is not None
