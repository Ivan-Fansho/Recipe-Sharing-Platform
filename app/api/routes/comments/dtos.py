from datetime import datetime

from pydantic import BaseModel


class CreateCommentDTO(BaseModel):
    recipe_id: int
    comment: str


class CommentShowDTO(BaseModel):
    username: str
    created_at: datetime
    comment: str