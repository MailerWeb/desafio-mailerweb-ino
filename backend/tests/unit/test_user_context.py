import pytest
from context.user.domain.entity.user import User
from context.user.errors.user import UserNotFound

# Teste de criação de User

def test_user_create():
    user = User.create(
        name="Usuário",
        email="user@example.com",
        password="senha123"
    )
    assert user.name == "Usuário"
    assert user.email == "user@example.com"

# Teste de erro UserNotFound

def test_user_not_found():
    with pytest.raises(UserNotFound):
        raise UserNotFound()
