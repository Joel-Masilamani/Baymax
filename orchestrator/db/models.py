# orchestrator/db/models.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# === User Model ===
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    records = relationship("MedicalRecord", back_populates="user")
    medications = relationship("MedicationSchedule", back_populates="user")


# === Medical Record Model ===
class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    diagnosis = Column(String(200))
    symptoms = Column(String(500))
    prescribed_medicines = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="records")


# === Medication Schedule Model ===
class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    medicine_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50))  # e.g. "once a day", "every 8 hours"
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    reminder_enabled = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="medications")
