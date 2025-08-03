from sqlmodel import SQLModel, Field, Relationship, String
from datetime import datetime
import uuid


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=200)
    created_at: datetime
    updated_at: datetime

    commodities: list["Commodity"] = Relationship(back_populates="category")


class Commodity(SQLModel, table=True):
    id: str | None = Field(default=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, max_length=200)
    specification: str | None = Field(max_length=200, default=None)
    category_id: int | None = Field(foreign_key="category.id")
    category: Category | None = Relationship(back_populates="commodities")
    created_at: datetime
    updated_at: datetime
