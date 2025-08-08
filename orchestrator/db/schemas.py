from pydantic import BaseModel
from typing import List
from datetime import date

class MedicalRecordOut(BaseModel):
    id: int
    user_id: int
    medicine_name: str
    dosage: str
    timings: List[str]
    start_date: date
    end_date: date

    model_config = {
        "from_attributes": True
    }
