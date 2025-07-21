from app.schemas.category import CategoryIn
from sqlmodel import Session, select
from app.models import Category
from datetime import datetime


def create_category(category, session: Session):
    new_category = Category(
        name=category.name, created_at=datetime.now(), updated_at=datetime.now())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


def list_categories(session: Session):
    categories = session.exec(select(Category)).all()
    return categories


def get_category(id: int, session: Session):
    category = session.get(Category, id)
    return category


def delete_category(category: Category, session: Session):
    session.delete(category)
    session.commit()
