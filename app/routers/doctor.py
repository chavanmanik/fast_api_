from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# ✅ Create appointment
@router.post("/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(database.get_db)):
    # Check patient & doctor exist
    patient = db.query(crud.models.Patient).filter(crud.models.Patient.id == appointment.patient_id).first()
    doctor = db.query(crud.models.Doctor).filter(crud.models.Doctor.id == appointment.doctor_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return crud.create_appointment(db, appointment)

# ✅ Get all appointments
@router.get("/", response_model=list[schemas.Appointment])
def get_all_appointments(db: Session = Depends(database.get_db)):
    return crud.get_appointments(db)

# ✅ Get appointment by ID
@router.get("/{appointment_id}", response_model=schemas.Appointment)
def get_appointment_by_id(appointment_id: int, db: Session = Depends(database.get_db)):
    appointment = db.query(crud.models.Appointment).filter(crud.models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# ✅ Delete appointment
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(database.get_db)):
    appointment = db.query(crud.models.Appointment).filter(crud.models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}
