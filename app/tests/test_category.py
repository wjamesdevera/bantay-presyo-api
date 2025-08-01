import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from ..db import get_session

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


def test_create_category(client: TestClient):
    response = client.post("/categories", json={"name": "Lowland Vegetable"})

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == "Lowland Vegetable"
    assert data["id"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
