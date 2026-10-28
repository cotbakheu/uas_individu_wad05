from collections.abc import Generator

from sqlalchemy.engine import make_url
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings

settings = get_settings()
database_url = settings.database_url
connect_args: dict[str, object] = {}

if database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
elif database_url.startswith("mysql"):
    parsed_url = make_url(database_url)
    query = dict(parsed_url.query)
    ssl_mode = query.pop("ssl-mode", query.pop("ssl_mode", None))
    database_url = parsed_url.set(query=query)

    if ssl_mode and str(ssl_mode).lower() in {"required", "true", "verify_ca", "verify_identity"}:
        connect_args["ssl"] = {}

engine = create_engine(database_url, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
