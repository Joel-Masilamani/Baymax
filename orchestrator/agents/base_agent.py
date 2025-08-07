import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load .env file when project starts
load_dotenv()

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("Missing environment variable: OPENROUTER_API_KEY")

    @abstractmethod
    async def process(self, user_input: str, context: dict):
        pass
