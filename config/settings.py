"""Configuration settings for the multi-agent system."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    openai_api_key: str
    openai_base_url: str = "https://api.aitunnel.ru/v1/"
    
    # Model configurations
    default_llm_model: str = "gpt-4-turbo-preview"
    
    # Tool configurations
    enable_web_search: bool = True
    enable_python_exec: bool = True
    max_tool_calls: int = 5
    
    # Agent configurations
    max_iterations: int = 10
    temperature: float = 0.7
    workspace_path: str = "/workspace"

    # OpenHands integration
    openhands_api_key: Optional[str] = None
    openhands_model: str = "openhands/claude-sonnet-4-5-20250929"
    openhands_llm_base_url: Optional[str] = None
    openhands_timeout_seconds: int = 180

    # Tester configuration
    tester_command: str = "pytest -q"
    tester_timeout_seconds: int = 180
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()

