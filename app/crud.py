from sqlalchemy.orm import Session
from . import models, schemas

# ---- PATIENT CRUD ----
def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patients(db: Session):
    return db.query(models.Patient).all()

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    if patient:
        db.delete(patient)
        db.commit()
        return True
    return False


# ---- DOCTOR CRUD ----
def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctors(db: Session):
    return db.query(models.Doctor).all()


# ---- APPOINTMENT CRUD ----
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session):
    return db.query(models.Appointment).all()
