from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import SavingsReport, User
from app.schemas import SavingsReportCreate, SavingsReportOut
from app.routes.auth import get_current_user, is_admin

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create savings report
@router.post("/", response_model=SavingsReportOut)
async def create_savings(
    savings: SavingsReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_savings = SavingsReport(**savings.dict(), user_id=current_user.id)
    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)
    return new_savings

# Get all savings reports for the logged-in user
@router.get("/", response_model=List[SavingsReportOut])
async def get_savings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    savings = db.query(SavingsReport).filter(SavingsReport.user_id == current_user.id).all()
    return savings

# Update savings report
@router.put("/{savings_id}", response_model=SavingsReportOut)
async def update_savings(
    savings_id: int,
    savings: SavingsReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_savings = db.query(SavingsReport).filter(
        SavingsReport.id == savings_id, SavingsReport.user_id == current_user.id
    ).first()
    if not db_savings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Savings report not found")

    for key, value in savings.dict().items():
        setattr(db_savings, key, value)
    
    db.commit()
    db.refresh(db_savings)
    return db_savings

# Delete savings report
@router.delete("/{savings_id}")
async def delete_savings(
    savings_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_savings = db.query(SavingsReport).filter(
        SavingsReport.id == savings_id, SavingsReport.user_id == current_user.id
    ).first()
    if not db_savings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Savings report not found")
    
    db.delete(db_savings)
    db.commit()
    return {"msg": "Savings report deleted successfully"}
