import logging
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    DEBUG: bool = False
    DATABASE_URL: str
    ALLOWED_ORIGINS: str

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v:str) -> List[str]:
        origins = v.split(",") if v else []
        logger.info(f"Configured CORS allowed origins: {origins}")
        return origins
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        

logger.info("Loading application settings from environment")
settings = Settings()
logger.info(f"Application settings loaded - DEBUG mode: {settings.DEBUG}")
