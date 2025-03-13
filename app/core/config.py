import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API настройки
    API_V1_STR: str = "/api/v1"
    
    # Безопасность
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30
    
    # Информация о приложении
    APP_NAME: str
    PROJECT_NAME: str = "Doors API"
    PROJECT_DESCRIPTION: str = "API для приложения Doors"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # База данных
    DB_URL: str
    DATABASE_URL: Optional[str] = None
    POSTGRES_SERVER: str = "localhost"  # значение по умолчанию
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        
        values = info.data
        # Если указан DATABASE_URL, используем его
        if values.get("DATABASE_URL"):
            return values.get("DATABASE_URL")
            
        # Иначе собираем URL из отдельных компонентов
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER", "localhost"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()