from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    email: EmailStr
    username: str
    name: str
    surname: str


class UserInDB(User):
    id: int
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    password: str
    role: str = "user"


class UserResponse(User):
    id: int

    model_config = ConfigDict(from_attributes=True)
