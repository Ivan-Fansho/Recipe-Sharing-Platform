from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import (
    String, Integer, Boolean, Text, ForeignKey, DateTime, create_engine, Column
)
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base( )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    profile_picture = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(100), nullable=False)
    ingredients = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    photo = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="recipes")


User.recipes = relationship("Recipe", order_by=Recipe.id, back_populates="user")


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)

    recipe = relationship("Recipe", back_populates="ratings")
    user = relationship("User", back_populates="ratings")


Recipe.ratings = relationship("Rating", order_by=Rating.id, back_populates="recipe")
User.ratings = relationship("Rating", order_by=Rating.id, back_populates="user")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    recipe = relationship("Recipe", back_populates="comments")
    user = relationship("User", back_populates="comments")


Recipe.comments = relationship("Comment", order_by=Comment.id, back_populates="recipe")
User.comments = relationship("Comment", order_by=Comment.id, back_populates="user")


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)

    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorites")


User.favorites = relationship("Favorite", order_by=Favorite.id, back_populates="user")
Recipe.favorites = relationship("Favorite", order_by=Favorite.id, back_populates="recipe")

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
