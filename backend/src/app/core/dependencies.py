from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session, select

from app.database.database import get_session
from app.models.user import User


def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    user = session.get(User, user_id)
    if not user:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User session is invalid")
    return user


def get_user_by_email(email: str, session: Session) -> User | None:
    return session.exec(select(User).where(User.email == email.lower())).first()
