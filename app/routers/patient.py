from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, auth

router = APIRouter(prefix="/patients", tags=["Patients"])

# -------------------- GET PATIENTS --------------------
@router.get("/", response_model=list[schemas.Patient])
def get_patients(
    db: Session = Depends(database.get_db),
    current_user: str = Depends(auth.get_current_user)
):
    return crud.get_patients(db)


# -------------------- CREATE PATIENT --------------------
@router.post("/", response_model=schemas.Patient)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(database.get_db),
    current_user: str = Depends(auth.get_current_user)
):
    return crud.create_patient(db, patient)


# -------------------- DELETE PATIENT --------------------
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(database.get_db),
    current_user: str = Depends(auth.get_current_user)
):
    if not crud.delete_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
