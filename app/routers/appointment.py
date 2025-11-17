from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# CREATE
@router.post("/", response_model=schemas.Appointment)
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    new_appt = models.Appointment(**appt.dict())
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)
    return new_appt


# GET ALL
@router.get("/", response_model=list[schemas.Appointment])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()


# UPDATE (FIX FOR YOU)
@router.put("/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(
    appointment_id: int,
    appt: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):
    db_appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for key, value in appt.dict().items():
        setattr(db_appt, key, value)

    db.commit()
    db.refresh(db_appt)
    return db_appt


# DELETE
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(db_appt)
    db.commit()
    return {"message": "Appointment deleted successfully"}
