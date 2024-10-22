from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@postgres:5432/bet_db"
    LINE_PROVIDER_URL: str = "http://line-provider:8000"

    class Config:
        env_file = ".env"


settings = Settings()
