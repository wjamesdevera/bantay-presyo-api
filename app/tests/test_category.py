from app.models import Category
import pytest
from fastapi.testclient import TestClient
from fastapi import responses, status
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from ..db import get_session
from datetime import datetime

from ..main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):

    def get_session_override():

        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


category_names = [
    "Imported Commercial Rice",
    "Local Commercial Rice",
    "Corn",
    "Fish",
    "Livestock & Poultry Products",
    "Lowland Vegetables",
    "Highland Vegetables",
    "Fruits",
    "Other Basic Commodities",
]


def generate_test_categories(session: Session):
    for category_name in category_names:
        category = Category(
            name=category_name, created_at=datetime.now(), updated_at=datetime.now()
        )
        session.add(category)
    session.commit


def test_create_category(client: TestClient):
    response = client.post("/categories", json={"name": "Spices"})

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == "Spices"
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_create_existing_category(client: TestClient, session: Session):
    generate_test_categories(session)
    response = client.post("/categories", json={"name": "Imported Commercial Rice"})

    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_category_invalid_name(client: TestClient):
    response = client.post("/categories", json={"name": ""})

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_read_all_category(session: Session, client: TestClient):
    generate_test_categories(session)
    response = client.get("/categories/")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 9
    for i, name in enumerate(category_names):
        assert data[i]["name"] == name


def test_read_single_category(session: Session, client: TestClient):
    generate_test_categories(session)
    response = client.get("/categories/1")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == 1
    assert data["name"] == category_names[0]


def test_reading_single_category_with_invalid_param(
    session: Session, client: TestClient
):
    generate_test_categories(session)
    response = client.get("/categories/hello")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_a_missing_category_return_a_404(session: Session, client: TestClient):
    generate_test_categories(session)
    response = client.get("/categories/100")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_updating_a_category(session: Session, client: TestClient):
    generate_test_categories(session)
    put_response = client.put("/categories/1", json={"name": "Spices"})
    put_data = put_response.json()

    assert put_response.status_code == status.HTTP_200_OK
    assert put_data["name"] == "Spices"

    get_response = client.get("/categories/1")
    get_data = get_response.json()

    assert get_response.status_code == status.HTTP_200_OK
    assert get_data["name"] == "Spices"


def test_updating_a_category_name_with_existing_name(
    session: Session, client: TestClient
):
    generate_test_categories(session)
    response = client.put("/categories/2", json={"name": "Imported Commercial Rice"})

    assert response.status_code == status.HTTP_409_CONFLICT


def test_updating_a_category_with_invalid_param(session: Session, client: TestClient):
    generate_test_categories(session)
    response = client.put("/categories/hello", json={"name": "Spices"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_updating_a_nonexistent_category(session: Session, client: TestClient):
    generate_test_categories(session)
    put_response = client.put("/categories/100", json={"name": "Spices"})

    assert put_response.status_code == status.HTTP_404_NOT_FOUND


def test_deleting_a_category(session: Session, client: TestClient):
    generate_test_categories(session)
    delete_response = client.delete("/categories/1")

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT


def test_deleting_a_category_with_invalid_param(session: Session, client: TestClient):
    generate_test_categories(session)
    response = client.put("/categories/hello")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_deleting_a_nonexistent_category(session: Session, client: TestClient):
    generate_test_categories(session)
    delete_response = client.delete("/categories/100")

    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
