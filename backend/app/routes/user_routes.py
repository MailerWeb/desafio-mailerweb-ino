from fastapi import APIRouter, Form, Depends
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from ..schemas.user import User
from ..schemas.form_login import FormLogin

user_router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.post("/login")
async def register_user(
    user_login: Annotated[FormLogin, Form()],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    return {"token": token, "login": user_login}


@user_router.post("/register")
async def register_user(user: User):
    return f"Usuário cadastrado com sucesso! {{'user': {user}}}"
