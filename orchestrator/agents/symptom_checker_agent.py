from .base_agent import BaseAgent
from .registry import register_agent
from typing import Dict, Any, Optional
import os
from openai import OpenAI

class SymptomCheckerAgent(BaseAgent):
    """
    Symptom Checker Agent (OpenRouter-powered):
    Uses LLM to analyze symptoms and suggest possible causes & advice.
    Falls back to a local mock mode if API key is missing.
    """
    name = "symptom_checker"

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")

        if api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
            self.model = "meta-llama/llama-3.1-70b-instruct"
            self.online_mode = True
        else:
            # Fallback mode without API key (for local dev)
            self.client = None
            self.online_mode = False

    async def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Handle empty input
        if not user_input.strip():
            return {
                "error": "No symptoms provided. Please describe your symptoms."
            }

        # 2. Online mode (real OpenRouter request)
        if self.online_mode:
            return await self._process_online(user_input)

        # 3. Offline mock mode
        return self._process_offline(user_input)

    async def _process_online(self, user_input: str) -> Dict[str, Any]:
        system_prompt = (
            "You are a helpful medical assistant. Given the symptoms, suggest 2–3 possible conditions, "
            "classify urgency (low/medium/high), and provide simple next steps. "
            "Keep it clear, friendly, and easy to understand. End with a short disclaimer."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )

            reply = response.choices[0].message.content.strip()

            return {
                "summary": reply,
                "notes": "Not a diagnosis. Consult a medical professional if concerned."
            }

        except Exception as e:
            return {"error": f"OpenRouter API call failed: {str(e)}"}

    def _process_offline(self, user_input: str) -> Dict[str, Any]:
        # Simple fallback for local testing
        return {
            "summary": (
                f"(Offline mode) Based on your symptoms: '{user_input}', "
                "you may have a mild common cold or flu. Drink plenty of fluids and rest."
            ),
            "notes": "Offline mock mode. No real AI processing was done."
        }

# Register agent
register_agent(SymptomCheckerAgent())
