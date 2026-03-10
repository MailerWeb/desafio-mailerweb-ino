from uuid import UUID
from pydantic import EmailStr, model_validator
from libs.model import Model


# ENTRADAS
class RegisterUserInput(Model):

    name: str
    email: EmailStr
    password: str

    @model_validator(mode="after")
    def validator(cls, data):
        if len(data.password) < 6:
            raise ValueError("Password must have at least 6 characters")
        if len(data.name) < 3:
            raise ValueError("Name must have at least 3 characters")

        return data


class SignInInput(Model):
    email: EmailStr
    password: str

    @model_validator(mode="after")
    def validator(cls, data):
        # TODO: USAR
        # if data.password and len(data.password) < 6:
        #     raise ValueError("Password must have at least 6 characters")
        return data


class Token(Model):
    access_token: str
    token_type: str


class UserOutPut(Model):
    id: UUID
    name: str
    email: EmailStr
