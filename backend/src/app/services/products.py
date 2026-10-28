from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate
from app.services.categories import require_category


def create_product(data: ProductCreate, user: User, session: Session) -> Product:
    require_category(data.category_id, user.id, session)
    values = data.model_dump()
    values["name"] = data.name.strip()
    product = Product(**values, owner_id=user.id)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def update_product(product_id: int, data: ProductCreate, user: User, session: Session) -> Product:
    product = session.exec(select(Product).where(Product.id == product_id, Product.owner_id == user.id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    require_category(data.category_id, user.id, session)
    for key, value in data.model_dump().items():
        setattr(product, key, value.strip() if isinstance(value, str) else value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def product_category_name(product: Product, session: Session) -> str:
    category = session.get(Category, product.category_id)
    return category.name if category else "Unknown"
