from pydantic import BaseModel
from datetime import datetime



# ===============================
#        PATIENT
class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    model_config = {"from_attributes": True}   # Pydantic v2


# ===============================
#        DOCTOR
class DoctorBase(BaseModel):
    name: str
    specialization: str
    phone: str

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int

    model_config = {"from_attributes": True}   # Pydantic v2


# ===============================
#       APPOINTMENT
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: datetime     
    reason: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    model_config = {"from_attributes": True}   # Pydantic v2


# ===============================
#          BILLING
class BillingBase(BaseModel):
    patient_id: int
    total_amount: float
    paid_amount: float
    payment_status: str = "Pending"

class BillingCreate(BillingBase):
    pass

class BillingResponse(BillingBase):
    id: int
    billing_date: datetime

    model_config = {"from_attributes": True}   


# ===============================
#           ROOM
class RoomBase(BaseModel):
    room_number: str
    room_type: str
    status: str = "Available"
    price_per_day: float

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int

    model_config = {"from_attributes": True}  