from fastapi import APIRouter

user_router = APIRouter(prefix="/user")


@user_router.get("/login")
def register_user():
    return "logando usuário"


@user_router.get("/register")
def register_user():
    return "registrando usuário"
