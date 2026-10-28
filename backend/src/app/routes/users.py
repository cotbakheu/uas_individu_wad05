from fastapi import APIRouter, Depends, Request

from app.core.dependencies import get_current_user
from app.middleware.csrf import ensure_csrf_token
from app.models.user import User
from app.schemas.auth import AuthResponse
from app.services.users import get_user_profile

router = APIRouter(prefix="/api/auth", tags=["users"])


@router.get("/me", response_model=AuthResponse)
def me(request: Request, user: User = Depends(get_current_user)):
    return AuthResponse(user=get_user_profile(user), csrf_token=ensure_csrf_token(request))
