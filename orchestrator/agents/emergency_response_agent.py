from .base_agent import BaseAgent
from .registry import register_agent
from typing import Dict, Any
import os
from openai import OpenAI

class EmergencyResponseAgent(BaseAgent):
    """
    Emergency Response Agent (LLM via OpenRouter):
    Evaluates health-related user inputs for urgency and guides on next immediate steps.
    """
    name = "emergency_response"

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
            "You are an emergency response assistant. Based on the user's input, "
            "evaluate how urgent the situation is and give a simple, clear recommendation. "
            "Your reply must include:\n"
            "1. Urgency Level: High / Medium / Low\n"
            "2. Immediate Action: What should the user do right now?\n"
            "3. Disclaimer: Always advise calling emergency services if needed."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5
            )

            reply = response.choices[0].message.content.strip()

            return {
                "response": reply
            }

        except Exception as e:
            return {"error": str(e)}

# Register agent
register_agent(EmergencyResponseAgent())
