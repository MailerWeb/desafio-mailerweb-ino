from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from typing import Annotated

from ..schemas.user import User
from ..schemas.form_login import FormLogin
from ..services import get_user, verify_password, create_access_token
from ..db import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.post("/login")
async def login_user(
    user_login: Annotated[FormLogin, Depends()], db: Session = Depends(get_db)
):
    user = get_user(db, user_login.username_email)

    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail/Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": user.username})

    return {
        "token": access_token,
        "token_type": "bearer",
    }


@user_router.post("/register")
async def register_user(user: User):
    return f"Usuário cadastrado com sucesso! {{'user': {user}}}"
