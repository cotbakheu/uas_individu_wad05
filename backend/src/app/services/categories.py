from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate


def require_category(category_id: int, owner_id: int, session: Session) -> Category:
    category = session.exec(select(Category).where(Category.id == category_id, Category.owner_id == owner_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(data: CategoryCreate, user: User, session: Session) -> Category:
    category = Category(name=data.name.strip(), owner_id=user.id)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def update_category(category_id: int, data: CategoryCreate, user: User, session: Session) -> Category:
    category = require_category(category_id, user.id, session)
    category.name = data.name.strip()
    session.add(category)
    session.commit()
    session.refresh(category)
    return category
