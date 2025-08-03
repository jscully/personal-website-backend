import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "Personal Website API"
    API_V1_STR: str = "/api"

    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    ALGORITHM: str = "HS256"

    CORS_ORIGINS: Union[str, List[str]] = ""

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "personal_website"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_URL: Optional[str] = None

    S3_BUCKET_NAME: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @model_validator(mode="after")
    def validate_db_connection(self) -> "Settings":
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        return self

    @model_validator(mode="after")
    def validate_elasticsearch_connection(self) -> "Settings":
        if not self.ELASTICSEARCH_URL:
            self.ELASTICSEARCH_URL = (
                f"http://{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}"
            )
        return self

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env.development",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

if settings.ENVIRONMENT == "development":
    settings.CORS_ORIGINS = settings.CORS_ORIGINS or [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
elif settings.ENVIRONMENT == "production":
    pass
