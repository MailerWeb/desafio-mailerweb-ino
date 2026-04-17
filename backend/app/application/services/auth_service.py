from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.application.interfaces.user_repository import AbstractUserRepository
from app.application.schemas.auth import LoginResponse, RegisterRequest, UserOut
from app.infrastructure.repositories.sqlalchemy_user_repo import UserRepositoryDep
from app.infrastructure.security.jwt import create_access_token, get_password_hash, verify_password
from app.infrastructure.database.models import UserModel


class AuthService:
    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo

    async def register(self, data: RegisterRequest) -> UserModel:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado.",
            )
        return await self.user_repo.create(
            name=data.name,
            email=data.email,
            password_hash=get_password_hash(data.password),
        )

    async def login(self, email: str, password: str) -> LoginResponse:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo.",
            )
        token = create_access_token(data={"sub": str(user.id)})
        return LoginResponse(access_token=token)


def get_auth_service(user_repo: UserRepositoryDep) -> AuthService:
    return AuthService(user_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
