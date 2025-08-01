from pydantic import BaseModel
from datetime import datetime

from app.schemas.category import CategoryOut


class CommodityOut(BaseModel):
    id: str
    name: str
    category_id: int
    category: CategoryOut
    created_at: datetime
    updated_at: datetime
