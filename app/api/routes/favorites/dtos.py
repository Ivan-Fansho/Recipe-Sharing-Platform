from datetime import datetime

from pydantic import BaseModel


class RecipeFavoriteSearchDTO(BaseModel):
    id: int
    title: str
    username: str
    category: str
    ingredients: str
    steps: str
    photo: str
    avg_rating: float
    created_at: datetime