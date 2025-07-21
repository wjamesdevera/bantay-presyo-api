from .base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Category(BaseModel):
    name: Mapped[str] = mapped_column(String(200))
