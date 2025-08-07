from .base_agent import BaseAgent
from .registry import register_agent
from typing import Dict, Any
import os
from openai import OpenAI

class MedicineInfoAgent(BaseAgent):
    """
    Medicine Info Agent (OpenRouter-powered):
    Provides usage, side effects, and safety information about medications.
    """
    name = "medicine_info"

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENROUTER_API_KEY environment variable")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        self.model = "meta-llama/llama-3.1-70b-instruct"

    async def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "You are a medical assistant providing safe, accurate medicine information. "
            "Explain usage, side effects, interactions, and precautions in simple terms. "
            "End with: 'Always consult a healthcare professional before taking any medication.'"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.6
            )

            reply = response.choices[0].message.content.strip()

            return {
                "medicine_info": reply
            }

        except Exception as e:
            return {"error": str(e)}

# Register the agent
register_agent(MedicineInfoAgent())
