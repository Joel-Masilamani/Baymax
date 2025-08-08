# routers/record_manager_router.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from orchestrator.db.schemas import MedicalRecordOut
from orchestrator.agents import record_manager
from orchestrator.db.database import get_db

router = APIRouter(prefix="/records", tags=["Record Manager"])

class RecordCreate(BaseModel):
    user_id: int
    medicine_name: str
    dosage: str
    timings: List[str]
    start_date: date
    end_date: date

@router.post("/", response_model=MedicalRecordOut)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    return record_manager.add_medical_record(db, **record.model_dump())


from fastapi import Query

@router.get("/active/{user_id}", response_model=List[MedicalRecordOut])
def get_active_records(
    user_id: int,
    current_date: date = date.today(),
    db: Session = Depends(get_db)
):
    return record_manager.get_active_medications(db, user_id=user_id, current_date=current_date)



@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    deleted = record_manager.delete_medical_record(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Deleted successfully"}

@router.get("/", response_model=List[MedicalRecordOut])
def get_all_records(db: Session = Depends(get_db)):
    return record_manager.get_all_records(db)

@router.get("/{record_id}", response_model=MedicalRecordOut)
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = record_manager.get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
