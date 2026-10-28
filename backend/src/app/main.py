from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.core.config import get_settings
from app.database.database import create_db_and_tables

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
