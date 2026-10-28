from fastapi import HTTPException
from sqlmodel import Session, select


def delete_owned(model: type, item_id: int, owner_id: int, session: Session) -> None:
    item = session.exec(select(model).where(model.id == item_id, model.owner_id == owner_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Resource not found")
    session.delete(item)
    session.commit()
