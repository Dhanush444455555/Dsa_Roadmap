import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "DSA Pathfinder"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://root:password@localhost:3306/dsa_pathfinder"
    )
    # Fallback to SQLite if MySQL is not reachable during local standalone testing
    USE_SQLITE_FALLBACK: bool = True
    SQLITE_URL: str = "sqlite:///./dsa_pathfinder.db"
    
    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dsa_pathfinder_super_secret_jwt_key_2026_change_in_production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")  # gemini, openai, ollama
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Email / SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAILS_FROM: str = os.getenv("EMAILS_FROM", "dsa-pathfinder@example.com")
    
    # File storage
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"
    )

settings = Settings()

# Ensure required directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
