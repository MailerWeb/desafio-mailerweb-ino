from uuid import UUID
from fastapi import APIRouter
from libs.output import OutputData
from libs.uow import UnitOfWork
from context.user.domain.command.user import RegisterUser, SignInUser, GetUserInfo
from context.user.domain.model.user import RegisterUserInput, SignInInput, Token, UserOutPut
from context.user.services.user import (
    register_user,
    user_login,
    get_logged_user,
)


route = APIRouter(tags=["users"], prefix="/users")


@route.post("/register")
def register_new_user(data: RegisterUserInput) -> OutputData[UserOutPut]:
    """Register a new user."""
    uow = UnitOfWork()

    command = RegisterUser(
        name=data.name,
        email=data.email,
        password=data.password,
    )

    user = register_user(command=command, uow=uow)

    user_output = UserOutPut(
        id=user.id,
        name=user.name,
        email=user.email,
    )

    return OutputData(data=user_output)


@route.post("/login")
def user_signin(data: SignInInput) -> OutputData[Token]:
    """Authenticate user and return access token."""
    uow = UnitOfWork()

    command = SignInUser(
        email=data.email,
        password=data.password,
    )

    token = user_login(command=command, uow=uow)

    return OutputData(data=token)


@route.get("/{user_id}")
def get_user_info(user_id: UUID) -> OutputData[UserOutPut]:
    """Retrieve information about a specific user."""
    uow = UnitOfWork()

    command = GetUserInfo(id_user=user_id)

    user = get_logged_user(command=command, uow=uow)

    user_output = UserOutPut(
        id=user.id,
        name=user.name,
        email=user.email,
    )

    return OutputData(data=user_output)
