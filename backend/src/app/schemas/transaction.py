from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.transaction import TransactionType


class TransactionCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    amount: int = Field(gt=0, description="Jumlah unit produk")
    type: TransactionType
    notes: str = Field(default="", max_length=500)
    transaction_date: datetime | None = None
    product_id: int = Field(gt=0)


class TransactionResponse(TransactionCreate):
    id: int
    total_amount: Decimal
