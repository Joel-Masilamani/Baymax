# agents/record_manager.py

from models import MedicalRecord, User
from db.database import get_db
from sqlalchemy.orm import Session
from datetime import date
from typing import List

def add_medical_record(db: Session, user_id: int, medicine: str, dosage: str, timings: List[str], start_date: date, end_date: date):
    record = MedicalRecord(
        user_id=user_id,
        medicine=medicine,
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
    records = db.query(MedicalRecord).filter(
        MedicalRecord.user_id == user_id,
        MedicalRecord.start_date <= current_date,
        MedicalRecord.end_date >= current_date
    ).all()
    return records


def delete_medical_record(db: Session, record_id: int):
    record = db.query(MedicalRecord).get(record_id)
    if record:
        db.delete(record)
        db.commit()
    return record
