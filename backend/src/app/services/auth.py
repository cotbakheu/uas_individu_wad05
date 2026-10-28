from sqlmodel import Session, select

from app.models.user import User


def get_user_by_email(email: str, session: Session) -> User | None:
    return session.exec(select(User).where(User.email == email.lower())).first()
