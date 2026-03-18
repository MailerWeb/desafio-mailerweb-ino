import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from typing import Annotated

from dotenv import load_dotenv

import logging

from ..models import UserDB, Token, TokenData
from ..schemas import UserInDB, User
from ..db import get_db

load_dotenv("../.env")

SECRET_KEY = os.getenv("API_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

password_helper = PasswordHash.recommended()


def get_user(db: Session, username: str):
    try:
        user = db.query(UserDB).filter(UserDB.username == username).first()

        if not user:
            logger.info("Usuário não encontrado. Retornando 'None'.")
            return None

        return UserInDB.model_validate(user)
    except SQLAlchemyError as e:
        logger.error(f"Erro ao buscar usuário de username {username}")
        raise e


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar a credencial!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        logger.error("Token inválido!")
        raise e

    user = get_user(db, token_data.username)

    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
