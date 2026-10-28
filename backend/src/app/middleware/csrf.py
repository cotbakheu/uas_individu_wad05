import secrets

from fastapi import HTTPException, Request, status

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
CSRF_EXEMPT_PATHS = {"/api/auth/login", "/api/auth/register"}


def ensure_csrf_token(request: Request) -> str:
    token = request.session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf_token"] = token
    return token


async def csrf_protection(request: Request, call_next):
    if request.method not in SAFE_METHODS and request.url.path not in CSRF_EXEMPT_PATHS:
        expected = request.session.get("csrf_token")
        supplied = request.headers.get("X-CSRF-Token")
        if not expected or not supplied or not secrets.compare_digest(expected, supplied):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")
    return await call_next(request)
