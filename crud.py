from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas

# Genre CRUD Operations

def create_genre(db: Session, genre: schemas.GenreCreate) -> models.Genre:
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def get_genre(db: Session, genre_id: int) -> Optional[models.Genre]:
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()

def get_genres(db: Session, skip: int = 0, limit: int = 10) -> List[models.Genre]:
    return db.query(models.Genre).offset(skip).limit(limit).all()

def delete_genre(db: Session, genre_id: int):
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre:
        db.delete(db_genre)
        db.commit()

# Actor CRUD Operations

def create_actor(db: Session, actor: schemas.ActorCreate) -> models.Actor:
    db_actor = models.Actor(**actor.model_dump())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

def get_actor(db: Session, actor_id: int) -> Optional[models.Actor]:
    return db.query(models.Actor).filter(models.Actor.id == actor_id).first()

def get_actors(db: Session, skip: int = 0, limit: int = 10) -> List[models.Actor]:
    return db.query(models.Actor).offset(skip).limit(limit).all()

def delete_actor(db: Session, actor_id: int):
    db_actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if db_actor:
        db.delete(db_actor)
        db.commit()

# Director CRUD Operations

def create_director(db: Session, director: schemas.DirectorCreate) -> models.Director:
    db_director = models.Director(**director.model_dump())
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

def get_director(db: Session, director_id: int) -> Optional[models.Director]:
    return db.query(models.Director).filter(models.Director.id == director_id).first()

def get_directors(db: Session, skip: int = 0, limit: int = 10) -> List[models.Director]:
    return db.query(models.Director).offset(skip).limit(limit).all()

def delete_director(db: Session, director_id: int):
    db_director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if db_director:
        db.delete(db_director)
        db.commit()

# Movie CRUD Operations

def create_movie(db: Session, movie: schemas.MovieCreate) -> models.Movie:
    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date,
        duration=movie.duration,
        rating=movie.rating,
        language=movie.language,
        poster_url=movie.poster_url,
        trailer_url=movie.trailer_url,
        genre_id=movie.genre_ids[0] if movie.genre_ids else None,
        director_id=movie.director_id
    )
    
    # Add actors to the movie
    if movie.cast_ids:
        db_movie.cast = db.query(models.Actor).filter(models.Actor.id.in_(movie.cast_ids)).all()
    
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movie_by_id(db: Session, movie_id: int) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 10) -> List[models.Movie]:
    return db.query(models.Movie).offset(skip).limit(limit).all()

def update_movie(db: Session, movie_id: int, movie_update: schemas.MovieUpdate) -> Optional[models.Movie]:
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not db_movie:
        return None
    
    for var, value in vars(movie_update).items():
        if value is not None:
            setattr(db_movie, var, value)
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        db.delete(db_movie)
        db.commit()

def delete_movie(db: Session, movie_id: int, user_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id, models.Movie.owner_id == user_id).first()
    if db_movie:
        db.delete(db_movie)
        db.commit()
    return db_movie

# Rating CRUD Operations

def create_rating(db: Session, rating: schemas.RatingCreate) -> models.Rating:
    db_rating = models.Rating(**rating.model_dump())

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_rating(db: Session, movie_id: int) -> Optional[models.Rating]:
    return db.query(models.Rating).filter(models.Rating.id == movie_id).first()

def get_ratings_for_movie(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()

def get_ratings(db: Session, skip: int = 0, limit: int = 10) -> List[models.Rating]:
    return db.query(models.Rating).offset(skip).limit(limit).all()

def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(models.Rating).filter(models.Rating.id == rating_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()

# User CRUD Operations

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str) -> models.User:
    db_user = models.User(username=user.username, 
                          email=user.email, 
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()

# Comment CRUD Operations
def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(**comment.model_dump(), user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_for_movie(db: Session, movie_id: int):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()

def get_comment_by_id(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()