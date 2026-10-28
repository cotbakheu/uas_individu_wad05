from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import get_settings
from app.database.database import create_db_and_tables
from app.middleware.csrf import csrf_protection
from app.routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-CSRF-Token"],
)
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=csrf_protection,
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie=settings.session_cookie_name,
    https_only=settings.session_cookie_secure,
    same_site=settings.session_cookie_samesite,
)

app.include_router(router)

frontend_dist = Path(__file__).resolve().parents[3] / "frontend" / "dist"
frontend_assets = frontend_dist / "assets"

if frontend_assets.is_dir():
    app.mount("/assets", StaticFiles(directory=frontend_assets), name="frontend-assets")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str):
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")
    index_file = frontend_dist / "index.html"
    if not index_file.is_file():
        raise HTTPException(status_code=404, detail="Frontend build not found")
    return FileResponse(index_file)
