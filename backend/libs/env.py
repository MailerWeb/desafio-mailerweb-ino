from pathlib import Path
from typing import Final
from pydantic_settings import BaseSettings
from pydantic import Field


def pegar_caminho_do_arquivo_env():
    return Path(__file__).parent.parent.parent / ".env"


print("Carregando ENV")


class GerenciadorENV(BaseSettings):
    _instancia = None

    # .json
    # GERAL
    AMBIENTE_ATUAL: Final[str] = Field(env="AMBIENTE_ATUAL")  # USADO TESTES
    PORT: Final[int] = Field(env="PORT")  # USADO
    HOST: Final[str] = Field(env="HOST")  # USADO

    # BANCO DE DADOS
    DB_CONNECTION: Final[str] = Field(env="DB_CONNECTION")  # Usado
    DB_HOST: Final[str] = Field(env="DB_HOST")  # Usado
    DB_PORT: Final[str] = Field(env="DB_PORT")  # Usado
    DB_USER: Final[str] = Field(env="DB_USER")  # Usado
    DB_PASSWORD: Final[str] = Field(env="DB_PASSWORD")  # Usado
    DB_DATABASE: Final[str] = Field(env="DB_DATABASE")  # Usado

    #
    SECRET_KEY: Final[str] = Field(env="SECRET_KEY")
    ALGORITHM: Final[str] = Field(env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = Field(env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # CELERY
    CELERY_BROKER_URL: Final[str] = Field(env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: Final[str] = Field(env="CELERY_RESULT_BACKEND")

    # EMAIL
    SMTP_SERVER: Final[str] = Field(env="SMTP_SERVER")
    SMTP_PORT: Final[int] = Field(env="SMTP_PORT")
    SMTP_USER: Final[str] = Field(env="SMTP_USER")
    SMTP_PASSWORD: Final[str] = Field(env="SMTP_PASSWORD")
    EMAIL_FROM: Final[str] = Field(env="EMAIL_FROM")

    # VIRTUAIS
    @property
    def DB_STRING_CONNECTION(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    @property
    def RAIZ_PROJETO_PATH(self):
        return Path(self.RAIZ_PROJETO)

    def print(self):
        print("-" * 95)
        for key, value in self.dict().items():
            print(f" - ENV: {key}: {value}")
        print("-" * 95)

    @classmethod
    def resetar(cls):
        cls._instancia = None
        cls._instancia = super().__new__(cls)

    class Config:
        env_file_encoding = "utf-8"
        env_file = pegar_caminho_do_arquivo_env()


ENVS = GerenciadorENV()