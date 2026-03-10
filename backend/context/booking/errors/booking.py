from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class BookingNotFound(HTTPException):
    status_code: int = 404
    detail: str = "Booking not found"


@dataclass
class BookingOverlap(HTTPException):
    status_code: int = 409
    detail: str = "Booking overlaps with existing booking"


@dataclass
class InvalidBookingTime(HTTPException):
    status_code: int = 400
    detail: str = "Invalid booking time"
    
