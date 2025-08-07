# orchestrator/db/init_db.py

from orchestrator.db.models import User, MedicalRecord, MedicationSchedule
from orchestrator.db.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully.")