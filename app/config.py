from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_FROM_NUMBER: Optional[str] = None
    TWILIO_MESSAGING_SERVICE_SID: Optional[str] = None
    TWILIO_VALIDATE_SIGNATURE: bool = True
    PUBLIC_BASE_URL: Optional[str] = None

    # App
    ENV: str = "dev"

    # Storage
    SQLITE_PATH: str = "./data/twilio.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
