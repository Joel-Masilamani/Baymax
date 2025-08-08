from ..agents.registry import get_agent
from ..models.request_models import ProcessRequest, ProcessResponse
from fastapi import HTTPException

async def route_to_agent(request: ProcessRequest) -> ProcessResponse:
    agent = get_agent(request.agent)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{request.agent}' not found.")
    
    result = await agent.process(request.user_input, request.context or {})
    return ProcessResponse(agent=request.agent, output=result)
