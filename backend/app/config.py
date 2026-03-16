import os
from dotenv import load_dotenv

import logging


logger = logging.getLogger("LOOGER")

load_dotenv(".env")


class Config:

    def __init__(self):
        self.DEBUG = os.getenv("DEBUG")

        self.APP_NAME = os.getenv("APP_NAME")
        self.API_KEY = os.getenv("API_KEY")

        if not self.API_KEY:
            if os.getenv("DEBUG") == "True":
                logger.warning(
                    "AVISO: Chave de acesso não definida e modo DEBUG == True! Usando chave de desenvolvimento."
                )
                self.API_KEY = "super_secret_key"
            else:
                raise ValueError(
                    "ERRO CRÍTICO: chave de acesso não definida no ambiente!"
                )

        self.USER_DB = os.getenv("USER_DB")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")

        self.REACT_PUBLIC_API_URL = os.getenv("REACT_PUBLIC_API_URL")
