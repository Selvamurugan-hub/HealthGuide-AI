import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env file from project root or backend directory if present
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class Settings(BaseModel):
    app_name: str = "HealthGuide AI"
    version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("PORT", "8000"))
    host: str = os.getenv("HOST", "127.0.0.1")
    cors_origins: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if origin.strip()
    ]
    ai_provider: str = os.getenv("AI_PROVIDER", "").strip().upper()
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    mask_user_input_in_logs: bool = os.getenv("MASK_USER_INPUT_IN_LOGS", "true").lower() in ("true", "1", "yes")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()


settings = Settings()
