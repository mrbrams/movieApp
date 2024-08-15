import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from .main import app, get_db
from . import models, schemas
from .database import Base

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new database session for each test
@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)  # Create the database tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Drop the database tables after tests

# Override the get_db dependency to use the testing session
@pytest.fixture(scope="module")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

# Test user creation
def test_create_user(client):
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

# Test token creation (login)
def test_login(client):
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Test movie creation
def test_create_movie(client):
    # First, log in to get a token
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Then, create a new movie
    response = client.post(
        "/movies/",
        json={"title": "Inception", "description": "A mind-bending thriller", "cast_ids": []},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception"
    assert data["description"] == "A mind-bending thriller"

# Test reading a movie
def test_read_movie(client):
    response = client.get("/movies/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception"
    assert data["description"] == "A mind-bending thriller"

# Test updating a movie
def test_update_movie(client):
    # First, log in to get a token
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Then, update the movie
    response = client.put(
        "/movies/1",
        json={"title": "Inception Updated", "description": "Updated description", "cast_ids": []},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception Updated"
    assert data["description"] == "Updated description"

# Test deleting a movie
def test_delete_movie(client):
    # First, log in to get a token
    login_response = client.post(
        "/token",
        data={"username": "testuser", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # Then, delete the movie
    response = client.delete(
        "/movies/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Verify that the movie is deleted
    response = client.get("/movies/1")
    assert response.status_code == 404
