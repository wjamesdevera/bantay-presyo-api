from pydantic import BaseModel
from datetime import datetime


class CategoryOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class CategoryIn(BaseModel):
    name: str
