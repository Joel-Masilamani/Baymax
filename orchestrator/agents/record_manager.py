from orchestrator.db.models import MedicalRecord
from sqlalchemy.orm import Session
from datetime import date
from typing import List

def add_medical_record(db: Session, user_id: int, medicine_name: str, dosage: str, timings: List[str], start_date: date, end_date: date):
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date.")
    record = MedicalRecord(
        user_id=user_id,
        medicine_name=medicine_name,
        dosage=dosage,
        timings=timings,
        start_date=start_date,
        end_date=end_date
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_active_medications(db: Session, user_id: int, current_date: date):
    return db.query(MedicalRecord).filter(
        MedicalRecord.user_id == user_id,
        MedicalRecord.start_date <= current_date,
        MedicalRecord.end_date >= current_date
    ).all()

def delete_medical_record(db: Session, record_id: int):
    record = db.get(MedicalRecord, record_id)
    if record:
        db.delete(record)
        db.commit()
    return record

def get_all_records(db: Session):
    return db.query(MedicalRecord).all()

def get_record_by_id(db: Session, record_id: int):
    return db.get(MedicalRecord, record_id)
