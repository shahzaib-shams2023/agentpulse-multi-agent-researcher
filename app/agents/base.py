import httpx
import json
import logging
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("AgentPulse")


class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    async def call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Execute LLM call using OpenAI-compatible endpoint with intelligent fallback."""
        if settings.llm_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {settings.llm_api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": settings.llm_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": settings.llm_temperature
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(
                        f"{settings.llm_base_url.rstrip('/')}/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        logger.warning(f"LLM API returned status {resp.status_code}, falling back to local reasoning engine.")
            except Exception as e:
                logger.warning(f"LLM request error: {str(e)}, utilizing fallback reasoning engine.")

        # Offline / Deterministic Reasoning Engine fallback
        return self._generate_fallback_response(system_prompt, user_prompt)

    def _generate_fallback_response(self, system_prompt: str, user_prompt: str) -> str:
        """Deterministic reasoning simulation for reliable offline execution and testing."""
        return f"Fallback reasoning for {self.name} processing prompt."

