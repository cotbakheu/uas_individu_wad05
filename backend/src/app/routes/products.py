from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlmodel import Session, select

from app.core.dependencies import get_current_user
from app.database.database import get_session
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse
from app.services.common import delete_owned
from app.services.products import create_product, product_category_name, update_product

router = APIRouter(prefix="/api/products", tags=["products"])


def product_response(product: Product, session: Session) -> ProductResponse:
    return ProductResponse(**product.model_dump(), category_name=product_category_name(product, session))


@router.get("", response_model=list[ProductResponse])
def list_products(
    search: str | None = Query(default=None, min_length=1, max_length=100),
    category_id: int | None = Query(default=None, gt=0),
    min_stock: int | None = Query(default=None, ge=0),
    max_stock: int | None = Query(default=None, ge=0),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Product).where(Product.owner_id == user.id)
    if search:
        term = f"%{search.strip()}%"
        statement = statement.where(or_(Product.name.ilike(term), Product.description.ilike(term)))
    if category_id:
        statement = statement.where(Product.category_id == category_id)
    if min_stock is not None:
        statement = statement.where(Product.stock >= min_stock)
    if max_stock is not None:
        statement = statement.where(Product.stock <= max_stock)
    return [product_response(item, session) for item in session.exec(statement.order_by(Product.name)).all()]


@router.post("", response_model=ProductResponse, status_code=201)
def add_product(payload: ProductCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return product_response(create_product(payload, user, session), session)


@router.put("/{product_id}", response_model=ProductResponse)
def edit_product(product_id: int, payload: ProductCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return product_response(update_product(product_id, payload, user, session), session)


@router.delete("/{product_id}", status_code=204)
def remove_product(product_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    delete_owned(Product, product_id, user.id, session)
