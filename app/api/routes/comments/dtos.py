from pydantic import BaseModel


class CreateCommentDTO(BaseModel):
    recipe_id: int
    comment: str
