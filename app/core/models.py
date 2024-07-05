from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped, mapped_column
from sqlalchemy import (
    String, Integer, Boolean, Text, ForeignKey, DateTime, create_engine, Column
)
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base( )

@dataclass
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(200), default=None, nullable=True)
    bio: Mapped[Text] = mapped_column(Text, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_restricted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    recipes: Mapped[list['Recipe']] = relationship("Recipe", back_populates="user")
    ratings: Mapped[list['Rating']] = relationship("Rating", back_populates="user")
    comments: Mapped[list['Comment']] = relationship("Comment", back_populates="user")
    favorites: Mapped[list['Favorite']] = relationship("Favorite", back_populates="user")

@dataclass
class Recipe(Base):
    __tablename__ = 'recipes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, ForeignKey('users.username'), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    ingredients: Mapped[Text] = mapped_column(Text, nullable=False)
    steps: Mapped[Text] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    photo: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="recipes")
    ratings: Mapped[list['Rating']] = relationship("Rating", back_populates="recipe")
    comments: Mapped[list['Comment']] = relationship("Comment", back_populates="recipe")
    favorites: Mapped[list['Favorite']] = relationship("Favorite", back_populates="recipe")

@dataclass
class Rating(Base):
    __tablename__ = 'ratings'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey('recipes.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="ratings")
    user: Mapped[User] = relationship("User", back_populates="ratings")

@dataclass
class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey('recipes.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    comment: Mapped[Text] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="comments")
    user: Mapped[User] = relationship("User", back_populates="comments")

@dataclass
class Favorite(Base):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey('recipes.id'), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="favorites")
    recipe: Mapped[Recipe] = relationship("Recipe", back_populates="favorites")

"""
Users Table:

    id (Primary Key)
    username
    email
    password
    profile_picture
    bio
    is_admin

Recipes Table:

    id (Primary Key)
    user_id (Foreign Key)
    title
    ingredients
    steps
    category
    photo
    created_at
    updated_at

Ratings Table:

    id (Primary Key)
    recipe_id (Foreign Key)
    user_id (Foreign Key)
    rating

Comments Table:

    id (Primary Key)
    recipe_id (Foreign Key)
    user_id (Foreign Key)
    comment
    created_at

Favorites Table:

    id (Primary Key)
    user_id (Foreign Key)
    recipe_id (Foreign Key)

"""
