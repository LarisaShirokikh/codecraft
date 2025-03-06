from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CodeCraft"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/codecraft"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    JWT_SECRET_KEY: str = "123456789"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()