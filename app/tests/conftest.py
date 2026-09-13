import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["TESTING"] = "sqlite://"

from database import Base, get_db
from main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_headers(client):
    test_user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass",
    }
    response = client.post("/users", json=test_user_data)
    assert response.status_code == 201
    login_response = client.post("/users/login", data={"username": test_user_data["username"], "password": test_user_data["password"]})
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}