import logging
from sqlalchemy.orm import Session

from app.api.routes.recipes.dtos import RecipeDTO
from app.api.routes.users.dtos import UserViewDTO
from app.core.db_dependency import get_db
from app.core.models import Recipe

logger = logging.getLogger(__name__)



def create(recipe: RecipeDTO, user: UserViewDTO, db: Session):


    new_recipe = Recipe(username=user.username, title=recipe.title,
                        ingredients=recipe.ingredients, steps=recipe.steps,
                        category=recipe.category, photo=recipe.photo )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe