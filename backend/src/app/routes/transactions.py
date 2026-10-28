from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.core.dependencies import get_current_user
from app.database.database import get_session
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transactions import create_transaction, delete_transaction, update_transaction

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


def serialize_transaction(transaction: Transaction, session: Session) -> dict:
    product = session.get(Product, transaction.product_id)
    return {
        **transaction.model_dump(),
        "total_amount": product.price * transaction.amount if product else 0,
    }


@router.get("", response_model=list[TransactionResponse])
def list_transactions(
    search: str | None = Query(default=None, min_length=1, max_length=100),
    transaction_type: str | None = Query(default=None, alias="type"),
    product_id: int | None = Query(default=None, gt=0),
    date_from: date | None = None,
    date_to: date | None = None,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Transaction).where(Transaction.owner_id == user.id)
    if search:
        statement = statement.where(Transaction.title.ilike(f"%{search.strip()}%"))
    if transaction_type in {"income", "expense"}:
        statement = statement.where(Transaction.type == transaction_type)
    if product_id:
        statement = statement.where(Transaction.product_id == product_id)
    if date_from:
        statement = statement.where(Transaction.transaction_date >= date_from)
    if date_to:
        statement = statement.where(Transaction.transaction_date < date_to.fromordinal(date_to.toordinal() + 1))
    transactions = session.exec(statement.order_by(Transaction.transaction_date.desc())).all()
    return [serialize_transaction(transaction, session) for transaction in transactions]


@router.post("", response_model=TransactionResponse, status_code=201)
def add_transaction(payload: TransactionCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return serialize_transaction(create_transaction(payload, user, session), session)


@router.put("/{transaction_id}", response_model=TransactionResponse)
def edit_transaction(transaction_id: int, payload: TransactionCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return serialize_transaction(update_transaction(transaction_id, payload, user, session), session)


@router.delete("/{transaction_id}", status_code=204)
def remove_transaction(transaction_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    delete_transaction(transaction_id, user, session)
