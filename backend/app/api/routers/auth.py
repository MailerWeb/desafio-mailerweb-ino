from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import CurrentUser
from app.application.schemas.auth import LoginResponse, RegisterRequest, UserOut
from app.application.services.auth_service import AuthServiceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(data: RegisterRequest, service: AuthServiceDep):
    user = await service.register(data)
    return user


@router.post("/login", response_model=LoginResponse)
async def login(
    service: AuthServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return await service.login(email=form_data.username, password=form_data.password)


@router.get("/me", response_model=UserOut)
async def me(current_user: CurrentUser):
    return current_user
