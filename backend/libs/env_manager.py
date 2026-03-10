from pathlib import Path
from typing import Final
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


def get_env_path():
    return Path(__file__).parent.parent / ".env"


class EnvManager(BaseSettings):
    _instancia = None

    # SERVIDOR
    PORT: int = Field(default=8000, env="PORT")
    HOST: str = Field(default="0.0.0.0", env="HOST")

    # BANCO DE DADOS
    DB_CONNECTION: str = Field(default="postgresql", env="DB_CONNECTION")
    DB_HOST: str = Field(default="postgres", env="DB_HOST")
    DB_PORT: str = Field(default="5432", env="DB_PORT")
    DB_USER: str = Field(default="postgres", env="DB_USER")
    DB_PASSWORD: str = Field(default="postgres", env="DB_PASSWORD")
    DB_DATABASE: str = Field(default="booking_db", env="DB_DATABASE")

    # AUTENTICAÇÃO
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # CELERY & REDIS
    CELERY_BROKER_URL: str = Field(default="redis://redis:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://redis:6379/1", env="CELERY_RESULT_BACKEND")

    # EMAIL
    SMTP_SERVER: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="your-email@gmail.com", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="your-app-password", env="SMTP_PASSWORD")
    EMAIL_FROM: str = Field(default="noreply@booking.local", env="EMAIL_FROM")

    # AMBIENTE
    AMBIENTE_ATUAL: str = Field(default="development", env="AMBIENTE_ATUAL")

    # VIRTUAIS
    @property
    def DB_STRING_CONNECTION(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    def print(self):
        print("-" * 95)
        for key, value in self.dict().items():
            print(f" - ENV: {key}: {value}")
        print("-" * 95)

    @classmethod
    def reset(cls):
        cls._instancia = None
        cls._instancia = super().__new__(cls)

    model_config = SettingsConfigDict(
        env_file=str(get_env_path()),
        env_file_encoding="utf-8",
        extra="ignore"
    )


ENVS = EnvManager()