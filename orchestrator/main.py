from fastapi import FastAPI
from .models.request_models import ProcessRequest, ProcessResponse
from .router import route_to_agent
from .agents.registry import list_agents  # New

# Import all agents (auto-register happens here)
from . import agents  # noqa: F401
from .routers import record_manager_router


app = FastAPI(title="Baymax Orchestrator", version="0.1")

app.include_router(record_manager_router.router)

@app.post("/process", response_model=ProcessResponse)
async def process_request(request: ProcessRequest):
    return await route_to_agent(request)

@app.get("/agents")
async def get_agents():
    return list_agents()

@app.get("/health")
async def health_check():
    return {"status": "Baymax orchestrator running"}
