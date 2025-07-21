from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.database import engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, func, String
from datetime import datetime

database_file = "db.sqlite3"
sql_database_url = f"sqlite:///{database_file}"

engine = create_engine(sql_database_url, echo=True)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), onupdate=func.now())


class Category(BaseModel):
    name: Mapped[str] = mapped_column(String(200))


BaseModel.metadata.create_all(bind=engine)
