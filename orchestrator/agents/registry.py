from typing import Dict
from .base_agent import BaseAgent

AGENT_REGISTRY: Dict[str, BaseAgent] = {}

def register_agent(agent: BaseAgent):
    if agent.name in AGENT_REGISTRY:
        raise ValueError(f"Agent '{agent.name}' already registered.")
    AGENT_REGISTRY[agent.name] = agent

def get_agent(agent_name: str) -> BaseAgent:
    return AGENT_REGISTRY.get(agent_name)

def list_agents() -> Dict[str, str]:
    """Return all registered agents and their docstrings."""
    return {name: agent.__doc__ for name, agent in AGENT_REGISTRY.items()}
