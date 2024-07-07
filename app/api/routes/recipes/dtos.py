from pydantic import BaseModel, field_validator



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