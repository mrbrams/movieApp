# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# import models, schemas, crud, auth, database
# from database import engine, SessionLocal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth import get_password_hash, verify_password, create_access_token, authenticate_user, verify_access_token, get_current_user, get_current_active_user
import crud as crud, schemas as schemas, models as models
from database import engine, Base, get_db
from auth import pwd_context
from typing import Optional
from logger import get_logger

logger = get_logger(__name__)


# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2PasswordBearer creates a login endpoint automatically at /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verify user credentials and return a user
def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user

# Endpoint to register a new user

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return crud.create_user(db, user)

# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
#     new_user = crud.create_user(db=db, user=user)
#     return new_user



@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info('Creating user...')
    db_user = crud.get_user_by_username(db, username=user.username)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        logger.warning(f"User with {user.username} already exists.")
        raise HTTPException(status_code=400, detail="Username already registered")
    logger.info('User successfully created.')
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

# Endpoint to get current logged-in user
@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

# Endpoint to obtain a token
@app.post("/login", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to create a movie
@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.create_movie(db=db, movie=movie)

# Endpoint to get a list of movies
@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

# Endpoint to get a specific movie added by ID (public access)
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# Endpoint to update a movie
# @app.put("/movies/{movie_id}", response_model=schemas.Movie)
# def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
#     return crud.update_movie(db=db, movie_id=movie_id, movie=movie)

@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    if db_movie.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this movie")
    
    return crud.update_movie(db=db, movie=movie, movie_id=movie_id, user_id=current_user.id)

# Endpoint to delete a movie
@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.delete_movie(db=db, movie_id=movie_id)

#Endpoint to delete a movie only by a user who listed it
@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    if db_movie.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this movie")
    
    deleted_movie = crud.delete_movie(db=db, movie_id=movie_id, user_id=current_user.id)
    if deleted_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return deleted_movie



#Endpoint to rate a movie
@app.post("/movies/{movie_id}/rate", response_model=schemas.Rating)
def rate_movie(movie_id: int, rating: schemas.RatingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    rating.movie_id = movie_id
    return crud.create_rating(db=db, rating=rating, user_id=current_user.id)

# Endpoint to get a list of movies rated by a user
@app.get("/movies/{movie_id}/ratings", response_model=list[schemas.Rating])
def get_ratings(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    return crud.get_ratings_for_movie(db=db, movie_id=movie_id)

# Endpoint to add a comment to a movie
@app.post("/movies/{movie_id}/comments", response_model=schemas.Comment)
def add_comment(movie_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    comment.movie_id = movie_id
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id)

# Endpoint to get a list of comments for a movie
@app.get("/movies/{movie_id}/comments", response_model=list[schemas.Comment])
def get_comments(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    return crud.get_comments_for_movie(db=db, movie_id=movie_id)

# Endpoint to add comment to a comment (nested comment)
@app.post("/comments/{comment_id}/reply", response_model=schemas.Comment)
def add_nested_comment(comment_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    comment.parent_id = comment_id
    comment.movie_id = db_comment.movie_id  # Ensure the movie ID is inherited
    return crud.create_comment(db=db, comment=comment, user_id=current_user.id)