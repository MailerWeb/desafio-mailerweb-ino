from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas.room import RoomCreate, RoomResponse
from ..services import room_services

from ..services import get_current_user

router = APIRouter(
    prefix="/rooms", tags=["Rooms"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return room_services.create_room(db=db, room=room)


@router.get("/", response_model=List[RoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    return room_services.get_rooms(db=db)


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return room_services.get_room_by_id(db=db, room_id=room_id)
