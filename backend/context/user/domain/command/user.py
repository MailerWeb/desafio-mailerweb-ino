from pydantic import EmailStr
from uuid import UUID
from libs.command import Command


class RegisterUser(Command):
    name: str
    email: EmailStr
    password: str


class SignInUser(Command):
    email: EmailStr
    password: str


class GetUserInfo(Command):
    id_user: UUID
