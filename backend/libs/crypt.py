from datetime import datetime, timedelta

import os
from typing import Any, Optional
from uuid import UUID

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password_hash(plain_password, hashed_password) -> Any:
    return bcrypt.verify(plain_password, hashed_password)


def generate_password_hash(password: str) -> str:
    return bcrypt.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")

    if not SECRET_KEY or not ALGORITHM:
        raise ValueError("SECRET_KEY and ALGORITHM must be defined in environment variables.")

    to_encode = data.copy()

    for key, value in to_encode.items():
        if isinstance(value, UUID):
            to_encode[key] = str(value)

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_token(token):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_identifier(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        identifier: str = payload.get("sub")

        if identifier is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    return identifier   