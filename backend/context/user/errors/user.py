from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class InvalidEmail(HTTPException):
    status_code: int = 400
    detail: str = "Invalid email"


@dataclass
class InvalidEmailOrPassword(HTTPException):
    status_code: int = 400
    detail: str = "Invalid email or password"


@dataclass
class UserWithSameEmail(HTTPException):
    status_code: int = 400
    detail: str = "There is already a user with that email"


@dataclass
class UserWithSameName(HTTPException):
    status_code: int = 400
    detail: str = "There is already a user with that name"


@dataclass
class ErrorCreatingUser(HTTPException):
    status_code: int = 500
    detail: str = "Error creating user"


@dataclass
class ErrorUpdatingUser(HTTPException):
    status_code: int = 500
    detail: str = "Error updating user"


@dataclass
class ErrorDeletingUser(HTTPException):
    status_code: int = 500
    detail: str = "Error deleting user"


@dataclass
class ErrorObtainingUser(HTTPException):
    status_code: int = 500
    detail: str = "Error obtaining user"


@dataclass
class UserNotFound(HTTPException):
    status_code: int = 404
    detail: str = "User not found"
