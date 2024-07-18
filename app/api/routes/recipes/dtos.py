from datetime import datetime

from pydantic import BaseModel, field_validator

from app.api.routes.comments.dtos import CommentShowDTO
from app.core.models import Comment


class RecipeDTO(BaseModel):
    title: str
    ingredients: str
    steps: str
    category: str
    photo: str

class RecipeUpdateDTO(BaseModel):
    title: str | None = None
    ingredients: str | None = None
    steps: str | None = None
    category: str | None = None
    photo: str | None = None

class RecipeShowDTO(BaseModel):
    title: str
    username: str
    category: str
    ingredients: str
    steps: str
    photo: str
    avg_rating: float
    created_at: datetime
    comments: list[CommentShowDTO]


class RecipeSearchDTO(BaseModel):
    id: int
    title: str
    username: str
    category: str
    ingredients: str
    steps: str
    photo: str
    avg_rating: float
    created_at: datetime
