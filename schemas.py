
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date, datetime
from typing import List, Optional

# Genre Schema
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True

# Actor Schema
class ActorBase(BaseModel):
    name: str
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int
    movies: List[int] = []

    class Config:
        orm_mode = True

# Director Schema
class DirectorBase(BaseModel):
    name: str
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int
    movies: List[int] = []

    class Config:
        orm_mode = True

# Movie Schema
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[date] = None
    duration: Optional[int] = None  # duration in minutes
    rating: Optional[float] = None
    genre_ids: List[int] = []
    director_id: Optional[int] = None
    cast_ids: List[int] = []
    language: Optional[str] = None
    # poster_url: Optional[str] = None
    trailer_url: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Rating Schema
class RatingBase(BaseModel):
    rating: int

class RatingCreate(RatingBase):
    movie_id: int

class Rating(RatingBase):
    id: int
    movie_id: int
    user_id: int

    class Config:
        orm_mode = True

# User Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    reviews: List[int] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    movie_id: Optional[int] = None
    parent_id: Optional[int] = None

class Comment(CommentBase):
    id: int
    movie_id: int
    user_id: int
    parent_id: Optional[int] = None
    replies: List["Comment"] = []

    class Config:
        orm_mode = True

Comment.update_forward_refs()