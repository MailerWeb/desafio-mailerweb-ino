from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.orm import Session

from typing import Annotated

from ..schemas import BookingCreate, BookingResponse
from ..db import get_db
from ..services import check_overlap, oauth2_scheme, get_current_user, authenticate_user

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@booking_router.post(
    "/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED
)
def post_booking(
    token: Annotated[str, Depends(oauth2_scheme)],
    booking: BookingCreate,
    db: Session = Depends(get_db),
):

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não está autorizado a acessar esta rota",
        )

    current_user_id = get_current_user(token=token, db=db).id

    new_booking = check_overlap(db, booking, user_id=current_user_id)

    return new_booking
