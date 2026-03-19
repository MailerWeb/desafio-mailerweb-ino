from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.room import Room
from app.schemas.room import RoomCreate


def create_room(db: Session, room: RoomCreate):
    existing_room = db.query(Room).filter(Room.name == room.name).first()
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma sala cadastrada com este nome.",
        )

    new_room = Room(name=room.name, capacity=room.capacity)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room


def get_rooms(db: Session):
    return db.query(Room).all()


def get_room_by_id(db: Session, room_id: int):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada."
        )
    return room
