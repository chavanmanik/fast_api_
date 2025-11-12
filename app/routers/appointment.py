from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# ✅ Create a doctor
@router.post("/", response_model=schemas.Doctor)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(database.get_db)):
    return crud.create_doctor(db, doctor)

# ✅ Get all doctors
@router.get("/", response_model=list[schemas.Doctor])
def get_all_doctors(db: Session = Depends(database.get_db)):
    return crud.get_doctors(db)

# ✅ Get single doctor by ID
@router.get("/{doctor_id}", response_model=schemas.Doctor)
def get_doctor_by_id(doctor_id: int, db: Session = Depends(database.get_db)):
    doctor = db.query(crud.models.Doctor).filter(crud.models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# ✅ Delete doctor
@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(database.get_db)):
    doctor = db.query(crud.models.Doctor).filter(crud.models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted successfully"}
