from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")

    energy_consumptions = relationship("EnergyConsumption", back_populates="user")
    savings_reports = relationship("SavingsReport", back_populates="user")

class EnergyConsumption(Base):
    __tablename__ = "energy_consumptions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    consumption = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    location = Column(String, nullable=False)
    remarks = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="energy_consumptions")

class SavingsReport(Base):
    __tablename__ = "savings_reports"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    energy_saved = Column(Float, nullable=False)
    savings = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    percentage_saved = Column(Float, nullable=False)
    units_saved = Column(Float, nullable=False)
    remarks = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="savings_reports")