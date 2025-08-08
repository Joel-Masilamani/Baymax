from datetime import datetime, date, time, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from typing import Optional, List, Union
from sqlalchemy import and_
from db.models import MedicalRecord, DoseStatus, DoseStatusEnum

class MedicineManagerService:

    def __init__(self, db: Session):
        self.db = db

    def get_active_records(self, user_id: int, on_date: Optional[date] = None) -> List[MedicalRecord]:
        """Get medicine records active on given date (default today)."""
        if on_date is None:
            on_date = date.today()
        return (
            self.db.query(MedicalRecord)
            .filter(
                MedicalRecord.user_id == user_id,
                MedicalRecord.start_date <= on_date,
                MedicalRecord.end_date >= on_date,
            )
            .all()
        )

    def generate_dose_datetimes(self, record: MedicalRecord, on_date: date) -> List[datetime]:
        """
        Given a record and date, generate datetime objects for each dose time.
        Assumes record.timings is a JSON list of time strings like ["08:00", "20:00"]
        """
        doses = []
        for timing_str in record.timings:
            hour, minute = map(int, timing_str.split(":"))
            dose_dt = datetime.combine(on_date, time(hour=hour, minute=minute))
            doses.append(dose_dt)
        return doses

    def create_doses_for_date(self, user_id: int, on_date: Optional[date] = None):
        """
        Generate DoseStatus entries for all active medicines on a given date,
        if they don't already exist.
        """
        if on_date is None:
            on_date = date.today()

        active_records = self.get_active_records(user_id, on_date)

        for record in active_records:
            dose_datetimes = self.generate_dose_datetimes(record, on_date)
            for dose_time in dose_datetimes:
                # Check if dose already exists
                existing_dose = (
                    self.db.query(DoseStatus)
                    .filter(DoseStatus.record_id == record.id, DoseStatus.dose_time == dose_time)
                    .first()
                )
                if not existing_dose:
                    new_dose = DoseStatus(
                        record_id=record.id,
                        dose_time=dose_time,
                        status=DoseStatusEnum.pending,
                    )
                    self.db.add(new_dose)
        self.db.commit()

    def get_pending_doses(self, user_id: int, from_datetime: Optional[datetime] = None) -> List[DoseStatus]:
        """Get all pending doses for a user from a given datetime onwards."""
        if from_datetime is None:
            from_datetime = datetime.now()

        doses = (
            self.db.query(DoseStatus)
            .join(MedicalRecord)
            .filter(
                MedicalRecord.user_id == user_id,
                DoseStatus.status == DoseStatusEnum.pending,
                DoseStatus.dose_time >= from_datetime,
            )
            .order_by(DoseStatus.dose_time)
            .all()
        )
        return doses

    def mark_dose_status(self, dose_id: int, status: DoseStatusEnum):
        """Mark a dose as taken or missed."""
        dose = self.db.query(DoseStatus).filter(DoseStatus.id == dose_id).first()
        if not dose:
            raise ValueError(f"DoseStatus with id {dose_id} not found")

        dose.status = status
        dose.marked_at = datetime.now()
        self.db.commit()
        return dose
    def get_next_upcoming_dose(self, user_id: int, from_datetime: Optional[datetime] = None) -> Optional[DoseStatus]:
        if from_datetime is None:
            from_datetime = datetime.now()
        return (
            self.db.query(DoseStatus)
            .join(MedicalRecord)
            .filter(
                MedicalRecord.user_id == user_id,
                DoseStatus.status == DoseStatusEnum.pending,
                DoseStatus.dose_time >= from_datetime,
            )
            .order_by(DoseStatus.dose_time.asc())
            .first()
        )

    def get_dose_history(
        self,
        user_id: int,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        record_id: Optional[int] = None,
    ) -> List[DoseStatus]:
        query = self.db.query(DoseStatus).join(MedicalRecord).filter(
            MedicalRecord.user_id == user_id,
            DoseStatus.status != DoseStatusEnum.pending,
        )

        if start_datetime:
            query = query.filter(DoseStatus.dose_time >= start_datetime)
        if end_datetime:
            query = query.filter(DoseStatus.dose_time <= end_datetime)
        if record_id:
            query = query.filter(DoseStatus.record_id == record_id)

        return query.order_by(DoseStatus.dose_time.desc()).all()

    def batch_mark_doses(
        self,
        dose_ids: List[int],
        status: DoseStatusEnum,
    ) -> int:
        """
        Mark multiple doses as taken or missed.
        Returns the count of updated doses.
        """
        updated = (
            self.db.query(DoseStatus)
            .filter(DoseStatus.id.in_(dose_ids))
            .update(
                {
                    DoseStatus.status: status,
                    DoseStatus.marked_at: datetime.now(),
                },
                synchronize_session=False,
            )
        )
        self.db.commit()
        return updated

    def cancel_future_doses(self, record_id: int, from_datetime: Optional[datetime] = None) -> int:
        """
        Cancel all future doses (e.g., mark missed) for a medicine record from given datetime onwards.
        Returns count of updated doses.
        """
        if from_datetime is None:
            from_datetime = datetime.now()

        updated = (
            self.db.query(DoseStatus)
            .filter(
                DoseStatus.record_id == record_id,
                DoseStatus.dose_time >= from_datetime,
                DoseStatus.status == DoseStatusEnum.pending,
            )
            .update(
                {
                    DoseStatus.status: DoseStatusEnum.missed,
                    DoseStatus.marked_at: datetime.now(),
                },
                synchronize_session=False,
            )
        )
        self.db.commit()
        return updated