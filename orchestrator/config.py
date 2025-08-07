# orchestrator/config.py
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("Missing environment variable: OPENROUTER_API_KEY")
