from .base_agent import BaseAgent
from .registry import register_agent
from typing import Dict, Any
import os
from openai import OpenAI

class FirstAidGuideAgent(BaseAgent):
    """
    First Aid Guide Agent (OpenRouter-powered):
    Provides step-by-step first aid instructions for emergencies.
    """
    name = "first_aid_guide"

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
            "You are a certified medical assistant providing first aid instructions. "
            "Given a scenario, offer clear, step-by-step guidance. Include safety warnings if needed. "
            "Always end with: 'This is not a substitute for professional care. Call emergency services if needed.'"
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
                "instructions": reply
            }

        except Exception as e:
            return {"error": str(e)}

# Register agent
register_agent(FirstAidGuideAgent())
