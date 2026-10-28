from decimal import Decimal
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=150, index=True)
    description: str = Field(default="", max_length=500)
    price: Decimal = Field(decimal_places=2, max_digits=12, ge=0)
    stock: int = Field(default=0, ge=0)
    owner_id: int = Field(foreign_key="users.id", index=True)
    category_id: int = Field(foreign_key="categories.id", index=True)

    owner: Optional["User"] = Relationship(back_populates="products")
    category: Optional["Category"] = Relationship(back_populates="products")
    transactions: list["Transaction"] = Relationship(back_populates="product")
