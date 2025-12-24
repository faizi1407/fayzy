from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fayzy"
    rate_limit: str = "5/minute"
    
    class Config:
        env_file = ".env"


settings = Settings()
