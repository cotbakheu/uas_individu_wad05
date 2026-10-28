from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.dependencies import get_current_user
from app.database.database import get_session
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.categories import create_category, update_category
from app.services.common import delete_owned

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(Category).where(Category.owner_id == user.id).order_by(Category.name)).all()


@router.post("", response_model=CategoryResponse, status_code=201)
def add_category(payload: CategoryCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return create_category(payload, user, session)


@router.put("/{category_id}", response_model=CategoryResponse)
def edit_category(category_id: int, payload: CategoryCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return update_category(category_id, payload, user, session)


@router.delete("/{category_id}", status_code=204)
def remove_category(category_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    delete_owned(Category, category_id, user.id, session)
