
from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class OutboxError(HTTPException):
    detail = "An error occurred while processing the outbox event"
    status_code: int = 500

