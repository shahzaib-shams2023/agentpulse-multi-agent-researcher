from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "AgentPulse Autonomous Multi-Agent Researcher"
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"

    # LLM Settings
    llm_api_key: Optional[str] = None
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2

    # Execution limits
    max_search_results: int = 5
    max_research_steps: int = 4

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
