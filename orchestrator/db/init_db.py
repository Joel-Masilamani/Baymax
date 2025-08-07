# orchestrator/db/init_db.py
from orchestrator.db.database import Base, engine
from orchestrator.db.models import user, project  # Add any models here

Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully.")
