from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    owner_id: int = Field(foreign_key="users.id", index=True)

    owner: Optional["User"] = Relationship(back_populates="categories")
    products: list["Product"] = Relationship(back_populates="category")
