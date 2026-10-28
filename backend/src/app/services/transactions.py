from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.product import Product
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate


def create_transaction(data: TransactionCreate, user: User, session: Session) -> Transaction:
    product = session.exec(select(Product).where(Product.id == data.product_id, Product.owner_id == user.id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    adjust_stock(product, data.type.value, data.amount)
    values = data.model_dump()
    values["transaction_date"] = values["transaction_date"] or datetime.now(timezone.utc)
    transaction = Transaction(**values, owner_id=user.id)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def update_transaction(transaction_id: int, data: TransactionCreate, user: User, session: Session) -> Transaction:
    transaction = session.exec(select(Transaction).where(Transaction.id == transaction_id, Transaction.owner_id == user.id)).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    old_product = session.exec(select(Product).where(Product.id == transaction.product_id, Product.owner_id == user.id)).first()
    new_product = session.exec(select(Product).where(Product.id == data.product_id, Product.owner_id == user.id)).first()
    if not old_product or not new_product:
        raise HTTPException(status_code=404, detail="Product not found")
    adjust_stock(old_product, transaction.type.value, -transaction.amount)
    try:
        adjust_stock(new_product, data.type.value, data.amount)
    except HTTPException:
        adjust_stock(old_product, transaction.type.value, transaction.amount)
        raise
    values = data.model_dump()
    values["transaction_date"] = values["transaction_date"] or transaction.transaction_date
    for key, value in values.items():
        setattr(transaction, key, value.strip() if isinstance(value, str) else value)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def adjust_stock(product: Product, transaction_type: str, quantity: int) -> None:
    stock_change = -quantity if transaction_type == "income" else quantity
    if product.stock + stock_change < 0:
        raise HTTPException(
            status_code=400,
            detail=f"Stok produk '{product.name}' tidak mencukupi. "
            f"Stok tersedia: {product.stock} unit, permintaan: {quantity} unit.",
        )
    product.stock += stock_change


def delete_transaction(transaction_id: int, user: User, session: Session) -> None:
    transaction = session.exec(
        select(Transaction).where(Transaction.id == transaction_id, Transaction.owner_id == user.id)
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    product = session.exec(
        select(Product).where(Product.id == transaction.product_id, Product.owner_id == user.id)
    ).first()
    if product:
        adjust_stock(product, transaction.type.value, -transaction.amount)
    session.delete(transaction)
    session.commit()
