from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/billing", tags=["Billing"])


# CREATE BILL
@router.post("/", response_model=schemas.BillingResponse)
def create_bill(bill: schemas.BillingCreate, db: Session = Depends(get_db)):
    new_bill = models.Billing(**bill.dict())
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill


# GET ALL BILLS
@router.get("/", response_model=list[schemas.BillingResponse])
def get_all_bills(db: Session = Depends(get_db)):
    return db.query(models.Billing).all()


# UPDATE BILL  ✅ REQUIRED BY FRONTEND
@router.put("/{bill_id}", response_model=schemas.BillingResponse)
def update_bill(bill_id: int, bill: schemas.BillingCreate, db: Session = Depends(get_db)):
    db_bill = db.query(models.Billing).filter(models.Billing.id == bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    for key, value in bill.dict().items():
        setattr(db_bill, key, value)

    db.commit()
    db.refresh(db_bill)
    return db_bill


# DELETE BILL  ✅ REQUIRED BY FRONTEND
@router.delete("/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    db_bill = db.query(models.Billing).filter(models.Billing.id == bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    db.delete(db_bill)
    db.commit()
    return {"message": "Bill deleted successfully"}
