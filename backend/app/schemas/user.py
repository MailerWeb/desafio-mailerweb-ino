from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    surname: str
    password: str
    email: str
    role: str


class UserCreator(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserInDB(User):
    hashed_password: str
