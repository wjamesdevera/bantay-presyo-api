from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship
from datetime import datetime
import uuid

sqlite_file_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: int | None = Field(
        default=None,
        primary_key=True
    )
    name: str = Field(
        index=True
    )
    created_at: datetime
    updated_at: datetime

    commodities: list["Commodity"] = Relationship(back_populates="categories")


class Commodity(SQLModel, table=True):
    __tablename__ = "commodities"
    id: str | None = Field(
        default=uuid.uuid4,
        primary_key=True
    )
    name: str = Field(
        index=True
    )
    category_id: int | None = Field(default=None, foreign_key="categories.id")
    category: Category | None = Relationship(back_populates="commodities")
    created_at: datetime
    updated_at: datetime


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
