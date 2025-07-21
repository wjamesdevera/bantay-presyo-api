from typing import List
from fastapi import APIRouter
from fastapi.routing import APIRoute
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(
    prefix="/categories"
)


class Category(BaseModel):
    id: int
    name: str
    createdAt: datetime
    updatedAt: datetime


sample_categories: List[Category] = [
    {
        "id": 1,
        "name": "Lowland Vegetables",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    },
    {
        "id": 2,
        "name": "Lowland Vegetables",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    },
    {
        "id": 3,
        "name": "Lowland Vegetables",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    },
]


def create_response_format(data: dict):
    return {
        "success": True,
        "data": data,
    }


@router.get("/")
def get_categories() -> List[Category]:
    return sample_categories
