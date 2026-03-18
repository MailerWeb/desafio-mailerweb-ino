from pydantic import BaseModel, EmailStr


class UserCreator(BaseModel):
    email: EmailStr
    username: str
    password: str
