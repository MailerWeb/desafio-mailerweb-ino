from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    surname: str
    password: str
    email: str
