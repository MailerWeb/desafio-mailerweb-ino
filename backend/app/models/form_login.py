from pydantic import BaseModel


class FormLogin(BaseModel):
    username_email: str
    password: str
