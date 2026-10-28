from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=150, index=True)
    amount: int = Field(gt=0, description="Jumlah unit produk")
    type: TransactionType = Field(index=True)
    notes: str = Field(default="", max_length=500)
    transaction_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    owner_id: int = Field(foreign_key="users.id", index=True)
    product_id: Optional[int] = Field(default=None, foreign_key="products.id", index=True)

    owner: Optional["User"] = Relationship(back_populates="transactions")
    product: Optional["Product"] = Relationship(back_populates="transactions")
