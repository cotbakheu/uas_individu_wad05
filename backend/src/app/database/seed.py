from sqlmodel import Session, select

from app.core.security import hash_password
from app.database.database import create_db_and_tables, engine
from app.models.category import Category
from app.models.user import User


def seed() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "admin@umkm.com")).first()
        if not user:
            user = User(
                name="Administrator UMKM",
                email="admin@umkm.com",
                password_hash=hash_password("Admin123!"),
                role="admin",
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        if not session.exec(
            select(Category).where(Category.owner_id == user.id)
        ).first():
            session.add_all(
                [
                    Category(name="Makanan", owner_id=user.id),
                    Category(name="Minuman", owner_id=user.id),
                    Category(name="Operasional", owner_id=user.id),
                ]
            )
            session.commit()


if __name__ == "__main__":
    seed()
