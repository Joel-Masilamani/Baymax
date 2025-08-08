from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey , Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base
from sqlalchemy import JSON
from datetime import datetime, timezone
import enum


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    records = relationship("MedicalRecord", back_populates="user")
    medications = relationship("MedicationSchedule", back_populates="user")

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    medicine_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    timings = Column(JSON, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    doses = relationship("DoseStatus", back_populates="record", cascade="all, delete-orphan")
    user = relationship("User", back_populates="records")

class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    medicine_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    reminder_enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="medications")

class DoseStatusEnum(str, enum.Enum):
    pending = "pending"
    taken = "taken"
    missed = "missed"

class DoseStatus(Base):
    __tablename__ = "dose_statuses"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=False)
    dose_time = Column(DateTime, nullable=False)
    status = Column(Enum(DoseStatusEnum), default=DoseStatusEnum.pending, nullable=False)
    marked_at = Column(DateTime, nullable=True)

    record = relationship("MedicalRecord", back_populates="doses")