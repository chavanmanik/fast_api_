from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from datetime import datetime
from sqlalchemy import DateTime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(225), nullable=False)


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(10))
    phone = Column(String(15))

    # ✅ FIX: Add missing appointments relationship
    appointments = relationship("Appointment", back_populates="patient")

    # billing relationship already correct
    billings = relationship("Billing", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    specialization = Column(String(50))
    phone = Column(String(15))

    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(DateTime)                     # <-- FIXED HERE
    reason = Column(String(255))

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    payment_status = Column(String(50), default="Pending")
    billing_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="billings")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(50), unique=True, nullable=False)
    room_type = Column(String(100), nullable=False)
    status = Column(String(50), default="Available")
    price_per_day = Column(Float, nullable=False)
