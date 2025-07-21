from pydantic import BaseModel
from datetime import datetime


class CategoryOut(BaseModel):
    id: int
    name: str
    createdAt: datetime
    updatedAt: datetime


class CategoryIn(BaseModel):
    name: str
