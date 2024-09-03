import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from .app.main import app  # Adjust the import based on your project structure
from .app.database import Base, get_db
from .app.models import Genre, Actor, Director, Movie, Rating, User, Comment
from .app.schemas import GenreCreate, ActorCreate, DirectorCreate, MovieCreate, RatingCreate, UserCreate, CommentCreate

# Define your test database URL
DATABASE_URL = "postgresql+asyncpg://postgres:1010@localhost/test_movie_database"

# Create a test database engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency override for test
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
async def setup_database():
    async with engine.begin() as conn:
        # Drop all tables and create them anew
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Teardown
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_genre(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/genres/", json={"name": "Action"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Action"}

@pytest.mark.asyncio
async def test_create_actor(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/actors/", json={"name": "John Doe", "date_of_birth": "1980-01-01", "bio": "An actor"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "date_of_birth": "1980-01-01", "bio": "An actor"}

@pytest.mark.asyncio
async def test_create_director(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/directors/", json={"name": "Jane Smith", "date_of_birth": "1975-05-01", "bio": "A director"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Jane Smith", "date_of_birth": "1975-05-01", "bio": "A director"}

@pytest.mark.asyncio
async def test_create_movie(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Make sure to have valid genre_id and director_id if necessary
        response = await client.post("/movies/", json={
            "title": "Epic Movie",
            "description": "An epic movie",
            "release_date": "2024-01-01",
            "duration": 120,
            "rating": 8.5,
            "genre_ids": [1],
            "director_id": 1,
            "cast_ids": [1],
            "language": "English",
            "trailer_url": "http://example.com/trailer"
        })
    assert response.status_code == 200
    assert response.json()["title"] == "Epic Movie"

@pytest.mark.asyncio
async def test_create_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_create_comment(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Make sure to have valid movie_id and user_id if necessary
        response = await client.post("/comments/", json={
            "content": "Great movie!",
            "movie_id": 1,
            "user_id": 1
        })
    assert response.status_code == 200
    assert response.json()["content"] == "Great movie!"
