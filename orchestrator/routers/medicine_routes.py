from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel, conint
from enum import Enum
from fastapi import Query
from typing import Optional
from pydantic import PositiveInt

from db.database import get_db
from orchestrator.agents.medicine_manager import MedicineManagerService
from db.models import DoseStatusEnum

router = APIRouter(prefix="/medicines", tags=["medicines"])

# --- Pydantic schemas ---

class DoseStatusStr(str, Enum):
    pending = "pending"
    taken = "taken"
    missed = "missed"

class DoseStatusResponse(BaseModel):
    id: int
    record_id: int
    dose_time: datetime
    status: DoseStatusStr
    marked_at: Optional[datetime]

    class Config:
        orm_mode = True

class MarkDoseRequest(BaseModel):
    dose_id: int
    status: DoseStatusStr

class BatchMarkDoseRequest(BaseModel):
    dose_ids: List[int]
    status: DoseStatusStr

# --- Routes ---

@router.get("/active", response_model=List[DoseStatusResponse])
def get_active_medicines(user_id: PositiveInt, db: Session = Depends(get_db)):
    """
    Get all pending doses for user (active medicines)
    """
    service = MedicineManagerService(db)
    doses = service.get_pending_doses(user_id)
    return doses


@router.get("/next-dose", response_model=DoseStatusResponse | None)
def get_next_dose(user_id: PositiveInt, db: Session = Depends(get_db)):
    """
    Get the next upcoming dose for user
    """
    service = MedicineManagerService(db)
    dose = service.get_next_upcoming_dose(user_id)
    if not dose:
        return None
    return dose


@router.post("/mark-dose", response_model=DoseStatusResponse)
def mark_dose(data: MarkDoseRequest, db: Session = Depends(get_db)):
    """
    Mark a single dose as taken or missed
    """
    service = MedicineManagerService(db)
    try:
        dose = service.mark_dose_status(data.dose_id, DoseStatusEnum(data.status))
        return dose
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/mark-doses-batch")
def batch_mark_doses(data: BatchMarkDoseRequest, db: Session = Depends(get_db)):
    """
    Mark multiple doses as taken or missed
    """
    service = MedicineManagerService(db)
    count = service.batch_mark_doses(data.dose_ids, DoseStatusEnum(data.status))
    return {"updated_count": count}


@router.post("/cancel-future-doses/{record_id}")
def cancel_future_doses(
    record_id: int,
    from_datetime: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Cancel future pending doses for a medicine record
    """
    service = MedicineManagerService(db)
    count = service.cancel_future_doses(record_id, from_datetime)
    return {"canceled_count": count}
