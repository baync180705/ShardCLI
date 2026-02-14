from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "llama-3.1-8b-instant"
    temperature: float = 0.0
    top_p: float = 0.9
    default_timeout_seconds: int = 30
    allow_high_risk_commands: bool = False

    model_config = {
        "env_file": BASE_DIR / ".env",
        "env_file_encoding": "utf-8"
    }
