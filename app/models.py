from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime

sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class Category(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True
    )
    name: str = Field(
        index=True
    )
    created_at: datetime
    updated_at: datetime


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
