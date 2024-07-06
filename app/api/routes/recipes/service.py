import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.routes.recipes.dtos import RecipeDTO
from app.api.routes.users.dtos import UserViewDTO
from app.api.utils.categories import categories
from app.core.db_dependency import get_db
from app.core.models import Recipe

logger = logging.getLogger(__name__)



def create(recipe: RecipeDTO, user: UserViewDTO, db: Session):

    try:
        if recipe.category.capitalize() not in categories:
            raise HTTPException(status_code=400, detail=
            "Category not supported please choole one of the available categories:"
            " [Pizzas, Soups, Deserts, Breakfast, Main Course, Appetizers, Beverages, Salads, Sandwiches]")

        new_recipe = Recipe(username=user.username, title=recipe.title,
                            ingredients=recipe.ingredients, steps=recipe.steps,
                            category=recipe.category, photo=recipe.photo )

        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Recipe could not be created")