from decimal import Decimal

from sqlmodel import Session, select

from app.models.product import Product
from app.models.transaction import Transaction


def dashboard_summary(user_id: int, session: Session) -> dict[str, Decimal | int]:
    transactions = session.exec(select(Transaction).where(Transaction.owner_id == user_id)).all()
    totals = [
        (item, session.get(Product, item.product_id))
        for item in transactions
    ]
    income = sum((product.price * item.amount for item, product in totals if product and item.type.value == "income"), Decimal("0"))
    expense = sum((product.price * item.amount for item, product in totals if product and item.type.value == "expense"), Decimal("0"))
    return {
        "income": income,
        "expense": expense,
        "balance": income - expense,
        "transaction_count": len(transactions),
        "product_count": len(session.exec(select(Product).where(Product.owner_id == user_id)).all()),
    }
