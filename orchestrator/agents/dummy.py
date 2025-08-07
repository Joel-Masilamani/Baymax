from .base_agent import BaseAgent
from .registry import register_agent
from typing import Any, Dict
import httpx

class DummyAgent(BaseAgent):
    """
    A simple OpenRouter-powered agent for testing Baymax orchestrator.
    """
    def __init__(self):
        super().__init__(name="dummy")

    async def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-4o-mini",  # or another OpenRouter-supported model
            "messages": [{"role": "user", "content": user_input}]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

        return {
            "message": data["choices"][0]["message"]["content"],
            "context_received": context
        }

# Register when imported
register_agent(DummyAgent())
