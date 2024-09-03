from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey, Table, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Association Table for many-to-many relationship between movies and actors
movie_actor_association = Table(
    'movie_actor', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
)

# Genre Model
class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    movies = relationship('Movie', secondary='movie_genre', back_populates='genres')
    
    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

# Actor Model
class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    bio = Column(Text)
    
    movies = relationship(
        "Movie",
        secondary=movie_actor_association,
        back_populates="cast"
    )

    def __repr__(self):
        return f"<Actor(id={self.id}, name='{self.name}')>"

# Director Model
class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    bio = Column(Text)
    
    movies = relationship("Movie", back_populates="director")

    def __repr__(self):
        return f"<Director(id={self.id}, name='{self.name}')>"

# Movie Model
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    release_date = Column(Date)
    duration = Column(Integer)
    rating = Column(Float)
    language = Column(String)
    poster_url = Column(String)
    trailer_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    genre_id = Column(Integer, ForeignKey('genres.id', ondelete='SET NULL'), index=True)
    director_id = Column(Integer, ForeignKey('directors.id', ondelete='SET NULL'), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    genre = relationship("Genre", back_populates="movies")
    director = relationship("Director", back_populates="movies")
    owner = relationship("User", back_populates="movies")
    ratings = relationship("Rating", back_populates="movie")
    comments = relationship("Comment", back_populates="movie")
    cast = relationship(
        "Actor",
        secondary=movie_actor_association,
        back_populates="movies"
    )
    genres = relationship('Genre', secondary='movie_genre', back_populates='movies')

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}')>"
  
class MovieGenre(Base):
    __tablename__ = 'movie_genre'
    
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)

# Rating Model
class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float)
    
    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")

    def __repr__(self):
        return f"<Rating(id={self.id}, movie_id={self.movie_id}, user_id={self.user_id}, rating={self.rating})>"

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    movies = relationship("Movie", back_populates="owner")
    ratings = relationship("Rating", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

#Comment Model
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    movie = relationship("Movie", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")

    def __repr__(self):
        return f"<Comment(id={self.id}, movie_id={self.movie_id}, user_id={self.user_id})>"