# orchestrator/db/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# ✅ Load .env file
load_dotenv()

# ✅ Get URL after loading env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file or environment variables.")

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
