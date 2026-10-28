from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session

from app.core.dependencies import get_current_user
from app.core.security import hash_password, verify_password
from app.database.database import get_session
from app.middleware.csrf import ensure_csrf_token
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.auth import get_user_by_email

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, session: Session = Depends(get_session)):
    if get_user_by_email(payload.email, session):
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(name=payload.name.strip(), email=payload.email.lower(), password_hash=hash_password(payload.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    request.session.clear()
    request.session["user_id"] = user.id
    return AuthResponse(user=user, csrf_token=ensure_csrf_token(request))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, request: Request, session: Session = Depends(get_session)):
    user = get_user_by_email(payload.email, session)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    request.session.clear()
    request.session["user_id"] = user.id
    return AuthResponse(user=user, csrf_token=ensure_csrf_token(request))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, _: User = Depends(get_current_user)):
    request.session.clear()

