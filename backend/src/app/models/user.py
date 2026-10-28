from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str
    role: str = Field(default="owner", max_length=30)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    categories: list["Category"] = Relationship(back_populates="owner")
    products: list["Product"] = Relationship(back_populates="owner")
    transactions: list["Transaction"] = Relationship(back_populates="owner")
