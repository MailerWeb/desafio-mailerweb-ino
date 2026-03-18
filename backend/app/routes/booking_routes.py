from fastapi import APIRouter, status, Depends

from sqlalchemy.orm import Session

from ..schemas import BookingCreate, BookingResponse
from ..db import get_db
from ..services import check_overlap

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@booking_router.post(
    "/create", response_model=BookingResponse, status_code=status.HTTP_201_CREATED
)
def post_booking(booking: BookingCreate, db: Session = Depends(get_db)):

    current_user_id = 1

    new_booking = check_overlap(db, booking, user_id=current_user_id)

    return new_booking
