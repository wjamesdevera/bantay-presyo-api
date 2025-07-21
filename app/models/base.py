from app.database import engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, func
from datetime import datetime


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), onupdate=func.now())


BaseModel.metadata.create_all(bind=engine)
