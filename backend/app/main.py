from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from contextlib import asynccontextmanager
import httpx

from .routes import ROUTERS
from .config import Config
from .db import engine, Base, get_db
from .models import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MEETING-APP")


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Iniciando aplicação...")
    try:
        limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
        app.state.http_client = httpx.AsyncClient(
            limits=limits, timeout=httpx.Timeout(10.0)
        )
        logger.info("Cliente HTTP assícrono inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Falha ao inicializar cliente persistente: {e}")

    logger.info("Iniciando conexão com os bancos de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL conectado com sucesso!")

    except Exception as e:
        logger.error(f"Falha ao conectar ao PostgreSQL: {e}")

    yield

    logger.info("Encerrando recursos...")
    await app.state.http_client.aclose()
    logger.info("Cliente HTTP encerrado com segurança.")


config = Config()

app = FastAPI(title=config.APP_NAME, debug=config.DEBUG, lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    config.REACT_PUBLIC_API_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in origins if origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in ROUTERS:
    app.include_router(router)
