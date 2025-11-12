from pydantic import BaseModel
from datetime import date

# --- Patient ---
class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True   # ✅ Replaces orm_mode in Pydantic v2


# --- Doctor ---
class DoctorBase(BaseModel):
    name: str
    specialization: str
    phone: str


class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase):
    id: int

    class Config:
        from_attributes = True   # ✅ Pydantic v2 fix


# --- Appointment ---
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    reason: str


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int

    class Config:
        from_attributes = True   # ✅ Pydantic v2 fix
