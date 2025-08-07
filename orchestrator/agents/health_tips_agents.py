from .base_agent import BaseAgent
from .registry import register_agent
from typing import Dict, Any
import os
from openai import OpenAI

class HealthTipsAgent(BaseAgent):
    """
    Health Tips Agent (LLM via OpenRouter):
    Provides short, actionable health advice based on user input or general wellness.
    """
    name = "health_tips"

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENROUTER_API_KEY environment variable")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = "mistralai/mixtral-8x7b-instruct"

    async def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "You are a friendly and knowledgeable health coach. "
            "Share 1–2 useful and science-backed health tips based on the user's goal or input. "
            "Tips should be practical, encouraging, and easy to follow. "
            "End with a light motivational line."
        )

        prompt = user_input or "Give me a general health tip."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )

            reply = response.choices[0].message.content.strip()

            return {
                "tips": reply
            }

        except Exception as e:
            return {"error": str(e)}

# Register the agent
register_agent(HealthTipsAgent())
