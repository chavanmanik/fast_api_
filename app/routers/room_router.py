from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/rooms", tags=["Rooms"])


# CREATE ROOM
@router.post("/", response_model=schemas.RoomResponse)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    new_room = models.Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


# SEARCH ROOM
@router.get("/search", response_model=list[schemas.RoomResponse])
def search_rooms(status: str = None, room_type: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Room)
    if status:
        query = query.filter(models.Room.status == status)
    if room_type:
        query = query.filter(models.Room.room_type == room_type)
    return query.all()


# UPDATE ROOM  ✅ (frontend calls this)
@router.put("/{room_id}", response_model=schemas.RoomResponse)
def update_room(room_id: int, room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    for key, value in room.dict().items():
        setattr(db_room, key, value)

    db.commit()
    db.refresh(db_room)
    return db_room


# DELETE ROOM  ✅ (frontend calls this)
@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(db_room)
    db.commit()
    return {"message": "Room deleted successfully"}
