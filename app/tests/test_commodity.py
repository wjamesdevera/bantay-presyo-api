from app.api import categories
from app.models import Commodity
import pytest
from fastapi.testclient import TestClient
from fastapi import responses, status
from sqlmodel import Session, create_engine, SQLModel, update
from sqlmodel.pool import StaticPool
from ..db import get_session
from datetime import datetime
from .test_category import generate_test_categories

from ..main import app


commodities = [
    {
        "name": "Fancy",
        "specification": "White Rice",
    },
    {
        "name": "Premium",
        "specification": "5% broken",
    },
    {
        "name": "Well Milled",
        "specification": "1-19% bran streak",
    },
    {
        "name": "Regular Milled",
        "specification": "20-40% bran streak",
    },
]


def generate_test_commodities(session: Session):
    for commodity in commodities:
        new_commodity = Commodity(
            name=commodity["name"],
            specification=commodity["specification"],
            category_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        session.add(new_commodity)

    session.commit()


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


# Test 1
# Test creation of valid commodity
def test_create_commodity(client: TestClient, session: Session):
    generate_test_categories(session)
    response = client.post(
        "/commodities/",
        json={"name": "Fancy", "specification": "White Rice", "category_id": 100},
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] is not None
    assert data["name"] == "Fancy"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_create_commodity_with_invalid_name(client: TestClient, session: Session):
    generate_test_categories(session)
    response = client.post(
        "/commodities/",
        json={"name": "", "specification": "White Rice", "category_id": 100},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_commodity_with_nonexistent_category(
    client: TestClient, session: Session
):
    generate_test_categories(session)
    response = client.post(
        "/commodities/",
        json={"name": "Fancy", "specification": "White Rice", "category_id": 100},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_commodity_that_exists(client: TestClient, session: Session):
    generate_test_categories(session)

    fancy = Commodity(
        name="Fancy",
        specification="White Rice",
        category_id=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(fancy)
    session.commit()

    response = client.post(
        "/commodities/",
        json={"name": "Fancy", "specification": "White Rice", "category_id": 100},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_read_categories(client: TestClient, session: Session):
    generate_test_categories(session)
    generate_test_commodities(session)

    response = client.get("/commodities/")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK

    for i, commodity in enumerate(commodities):
        assert data[i]["name"] == commodity["name"]
        assert data[i]["specification"] == commodity["specification"]
