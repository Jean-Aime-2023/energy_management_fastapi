from pydantic import BaseModel
from datetime import date, time
from typing import Optional

# User schemas
# Login request schema
class LoginRequest(BaseModel):
    username: str
    password: str

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class EnergyConsumptionCreate(BaseModel):
    date: date
    time: time
    consumption: float
    cost: float
    source: str
    location: str
    remarks: Optional[str] = None

class EnergyConsumptionOut(EnergyConsumptionCreate):
    id: int

    class Config:
        orm_mode = True

# Savings report schemas
class SavingsReportCreate(BaseModel):
    date: date
    energy_saved: float
    savings: float
    method: str
    percentage_saved: float
    units_saved: float
    remarks: Optional[str] = None

class SavingsReportOut(SavingsReportCreate):
    id: int

    class Config:
        orm_mode = True