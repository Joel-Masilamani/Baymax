from pydantic import BaseModel
from typing import Optional, Dict, Any

class ProcessRequest(BaseModel):
    agent: str  # Which agent to call
    user_input: str
    context: Optional[Dict[str, Any]] = {}

class ProcessResponse(BaseModel):
    agent: str
    output: Dict[str, Any]
