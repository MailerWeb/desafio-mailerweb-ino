from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class RoomNotFound(HTTPException):
    def __init__(self, detail: str, status_code: int = 404):
        self.detail = detail
        self.status_code = status_code


@dataclass
class RoomNameExists(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
