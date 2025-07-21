from typing import List
from fastapi import APIRouter, HTTPException
from datetime import datetime
from fastapi import status
from app.schemas.category import CategoryIn, CategoryOut
from app.services import category as category_service
from app.models import SessionDep

router = APIRouter(
    prefix="/categories",
)


@router.get("/", response_model=List[CategoryOut])
def get_categories(session: SessionDep) -> List[CategoryOut]:
    return category_service.list_categories(session=session)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryIn, session: SessionDep) -> CategoryOut:
    new_category = category_service.create_category(category, session)
    return new_category


@router.get("/{id}", response_model=CategoryOut)
def category_detail(id: int, session: SessionDep) -> CategoryOut:
    category = category_service.get_category(id, session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return category


@router.put("/{id}", response_model=CategoryOut)
def update_category(id: int, category: CategoryIn, session: SessionDep) -> CategoryOut:
    old_category = category_service.get_category(id, session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    new_category = category_service.update_category(
        old_category, category, session)
    return new_category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, session: SessionDep):
    category = category_service.get_category(id, session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    category_service.delete_category(category, session)
    return {
        "success": True
    }
