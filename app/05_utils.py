from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    
    log_level: str = "info"
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()