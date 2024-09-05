from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRequest(BaseModel):
    username: str
    password: str

# Genre Schema
class GenreBase(BaseModel):
    name: str = Field(..., description="Name of the genre")

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int = Field(..., description="Unique identifier for the genre")

    class Config:
        from_attributes = True

# Actor Schema
class ActorBase(BaseModel):
    name: str = Field(..., description="Name of the actor")
    date_of_birth: Optional[date] = Field(None, description="Date of birth of the actor")
    bio: Optional[str] = Field(None, description="Biography of the actor")

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int = Field(..., description="Unique identifier for the actor")
    movies: List[int] = Field(default=[], description="List of movie IDs the actor has appeared in")

    class Config:
        from_attributes = True

# Director Schema
class DirectorBase(BaseModel):
    name: str = Field(..., description="Name of the director")
    date_of_birth: Optional[date] = Field(None, description="Date of birth of the director")
    bio: Optional[str] = Field(None, description="Biography of the director")

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int = Field(..., description="Unique identifier for the director")
    movies: List[int] = Field(default=[], description="List of movie IDs directed by the director")

    class Config:
        from_attributes = True

# Movie Schema
class MovieBase(BaseModel):
    title: str = Field(..., description="Title of the movie")
    description: Optional[str] = Field(None, description="Description of the movie")
    release_date: Optional[date] = Field(None, description="Release date of the movie")
    duration: Optional[int] = Field(None, description="Duration of the movie in minutes")
    rating: Optional[float] = Field(None, description="Rating of the movie")
    genre_ids: Optional[List[int]] = Field(default=[], description="List of genre IDs associated with the movie")
    director_id: Optional[int] = Field(None, description="ID of the director of the movie")
    # cast_ids: Optional[List[int]] = Field(default=[], description="List of actor IDs who acted in the movie")
    language: Optional[str] = Field(None, description="Language of the movie")
    trailer_url: Optional[str] = Field(None, description="URL of the movie trailer")

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class Movie(MovieBase):
    id: int = Field(..., description="Unique identifier for the movie")
    created_at: datetime = Field(..., description="Timestamp when the movie was created")
    updated_at: datetime = Field(..., description="Timestamp when the movie was last updated")

    class Config:
        from_attributes = True

# Rating Schema
class RatingBase(BaseModel):
    rating: float = Field(..., description="Rating given to the movie")

class RatingCreate(RatingBase):
    movie_id: int = Field(..., description="ID of the movie being rated")

class Rating(RatingBase):
    id: int = Field(..., description="Unique identifier for the rating")
    movie_id: int = Field(..., description="ID of the movie being rated")
    user_id: int = Field(..., description="ID of the user who gave the rating")

    class Config:
       from_attributes = True

# User Schema
class UserBase(BaseModel):
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")

class UserCreate(UserBase):
    password: str = Field(..., description="Password of the user")

class User(UserBase):
    id: int = Field(..., description="Unique identifier for the user")
    password_hash: str = Field(..., description="Hashed password of the user")  
    is_active: bool = Field(default=True, description="Indicates if the user is active")
    comments: List[int] = Field(default=[], description="List of comment IDs made by the user")

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of the token")

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")

class CommentBase(BaseModel):
    content: str = Field(..., description="Content of the comment")

class CommentCreate(CommentBase):
    movie_id: Optional[int] = Field(None, description="ID of the movie the comment is related to")
    parent_id: Optional[int] = Field(None, description="ID of the parent comment if it is a reply")

class Comment(CommentBase):
    id: int = Field(..., description="Unique identifier for the comment")
    movie_id: int = Field(..., description="ID of the movie the comment is related to")
    user_id: int = Field(..., description="ID of the user who made the comment")
    parent_id: Optional[int] = Field(None, description="ID of the parent comment if it is a reply")
    replies: List["Comment"] = Field(default=[], description="List of replies to this comment")

    class Config:
       from_attributes = True

Comment.update_forward_refs()
