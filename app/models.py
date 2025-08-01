from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime
    updated_at: datetime

    commodities: list["Commodity"] = Relationship(back_populates="category")


class Commodity(SQLModel, table=True):
    id: str | None = Field(default=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: Category | None = Relationship(back_populates="commodities")
    created_at: datetime
    updated_at: datetime
