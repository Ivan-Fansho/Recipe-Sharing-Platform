from pydantic import BaseModel, field_validator



class RecipeDTO(BaseModel):
    title: str
    ingredients: str
    steps: str
    category: str
    photo: str