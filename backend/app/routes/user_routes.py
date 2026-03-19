from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from typing import Annotated

from ..models import UserDB
from ..schemas import UserCreate
from ..schemas import FormLogin
from ..services import get_user, verify_password, create_access_token, get_password_hash
from ..db import get_db

import logging

logger = logging.getLogger(__name__)

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
async def register_user(
    db: Annotated[Session, Depends(get_db)], user_create: UserCreate
):
    logger.info(user_create)
    if get_user(db, username_email=user_create.username) or get_user(
        db, username_email=user_create.email
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ou e-mail já cadastrados!",
        )

    hashed_password = get_password_hash(user_create.password)

    new_user = UserDB(
        username=user_create.username,
        email=user_create.email,
        name=user_create.name,
        surname=user_create.surname,
        hashed_password=hashed_password,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        logger.error({e})
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar usuário!",
        )
