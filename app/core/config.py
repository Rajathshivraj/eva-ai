
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "EVA - Exploratory Visualization & AutoML Assistant"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    VERSION: str = "0.1.0"
    
    # File Storage
    UPLOAD_DIR: str = "data/uploads"
    OUTPUT_DIR: str = "data/outputs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
