from datetime import datetime

from pydantic import BaseModel


class UserAdminViewDTO(BaseModel):
    id: int
    username: str
    email: str
    profile_picture: str | None = None
    bio: str | None = None
    is_restricted: bool


class CommentAdminShowDTO(BaseModel):
    comment_id: int
    username: str
    recipe_id: int
    created_at: datetime
    comment: str