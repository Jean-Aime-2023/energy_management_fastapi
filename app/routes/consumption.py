from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal  
from app.models import EnergyConsumption, User
from app.schemas import EnergyConsumptionCreate, EnergyConsumptionOut
from app.routes.auth import get_current_user, is_admin

router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EnergyConsumptionOut)
async def create_consumption(
    consumption: EnergyConsumptionCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_consumption = EnergyConsumption(**consumption.dict(), user_id=current_user.id)
    db.add(new_consumption)
    db.commit()
    db.refresh(new_consumption)
    return new_consumption

@router.get("/", response_model=List[EnergyConsumptionOut])
async def get_consumptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    consumptions = db.query(EnergyConsumption).filter(EnergyConsumption.user_id == current_user.id).all()
    return consumptions

@router.put("/{consumption_id}", response_model=EnergyConsumptionOut)
async def update_consumption(
    consumption_id: int,
    consumption: EnergyConsumptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_consumption = db.query(EnergyConsumption).filter(
        EnergyConsumption.id == consumption_id, EnergyConsumption.user_id == current_user.id
    ).first()
    if not db_consumption:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consumption not found")

    for key, value in consumption.dict().items():
        setattr(db_consumption, key, value)
    
    db.commit()
    db.refresh(db_consumption)
    return db_consumption

@router.delete("/{consumption_id}")
async def delete_consumption(
    consumption_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_consumption = db.query(EnergyConsumption).filter(
        EnergyConsumption.id == consumption_id, EnergyConsumption.user_id == current_user.id
    ).first()
    if not db_consumption:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consumption not found")
    
    db.delete(db_consumption)
    db.commit()
    return {"msg": "Consumption deleted successfully"}

@router.get("/admin-only-route")
async def admin_only_route(current_user: User = Depends(is_admin)):
    return {"msg": "Welcome, Admin!"}
