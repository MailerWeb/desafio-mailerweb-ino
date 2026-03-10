
from typing import Optional

from libs.crypt import create_access_token
from context.user.errors.user import (
    ErrorObtainingUser,
    InvalidEmailOrPassword,
    UserWithSameEmail,
)
from libs.uow import UnitOfWorkAbstract
from context.user.repository.repo.user_repo import UserRepo
from context.user.domain.command.user import RegisterUser, SignInUser, GetUserInfo
from context.user.domain.entity.user import User
from context.user.domain.model.user import Token


def register_user(command: RegisterUser, uow: UnitOfWorkAbstract):
    """Register a new user."""
    user = User.create(
        name=command.name,
        email=command.email,
        password=command.password,
    )

    with uow:
        repo = UserRepo(uow.session)

        email_exists = repo.search_by_email(user.email)

        if email_exists:
            raise UserWithSameEmail(detail="Email already registered", status_code=400)

        repo.add(user)
        uow.commit()

    return user


def user_login(command: SignInUser, uow: UnitOfWorkAbstract):
    """Authenticate user and return access token."""
    with uow:
        repo = UserRepo(uow.session)

        user = repo.search_by_email(command.email)

        if not user:
            raise InvalidEmailOrPassword(detail="Invalid email or password", status_code=400)

        if not user.verify_password(command.password):
            raise InvalidEmailOrPassword(detail="Invalid email or password", status_code=400)

    token_created = create_access_token({"sub": user.id})

    return Token(access_token=token_created, token_type="bearer")


def get_logged_user(
    command: GetUserInfo, uow: UnitOfWorkAbstract
) -> User:
    """Retrieve information about the logged-in user."""
    with uow:
        repo = UserRepo(uow.session)
        user: Optional[User] = repo.search_by_id(command.id_user)

        if not user:
            raise ErrorObtainingUser(detail="User not found", status_code=404)

    return user
