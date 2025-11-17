from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.database import engine, Base
from app.routers import billing_router, room_router, patient, doctor, appointment, auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app (only once ✅)
app = FastAPI(title="Hospital Management System")

# Include routers
app.include_router(billing_router.router)
app.include_router(room_router.router)
app.include_router(auth_router.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
def serve_frontend():
    return FileResponse(os.path.join("static", "index.html"))
