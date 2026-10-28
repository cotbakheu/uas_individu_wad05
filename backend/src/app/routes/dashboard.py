from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.dependencies import get_current_user
from app.database.database import get_session
from app.models.user import User
from app.services.dashboard import dashboard_summary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return dashboard_summary(user.id, session)
