from fastapi import HTTPException

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.api.routes.favorites.dtos import RecipeFavoriteSearchDTO
from app.api.routes.recipes.dtos import RecipeSearchDTO
from app.api.routes.recipes.service import get_avg_rating
from app.api.utils.categories import categories
from app.api.utils.custom_errors import RecipeNotFoundException, FavoriteAlreadyExistsException, \
    FavoriteDoesntExistsException, WrongCategoryException
import logging

from app.core.models import Recipe, Favorite, User

logger = logging.getLogger(__name__)


def add_fav(user_id, recipe_id, db):
    try:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise RecipeNotFoundException()
        favorite_exists = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.recipe_id == recipe_id).first()
        if favorite_exists:
            raise FavoriteAlreadyExistsException()
        new_favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
        db.add(new_favorite)
        db.commit()
        return recipe.title
    except RecipeNotFoundException as e:
        logger.error(e)
        raise e
    except FavoriteAlreadyExistsException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e


def remove_fav(user_id, recipe_id, db):
    try:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise RecipeNotFoundException()
        favorite_exists = db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.recipe_id == recipe_id).first()
        if not favorite_exists:
            raise FavoriteDoesntExistsException()
        db.delete(favorite_exists)
        db.commit()
        return recipe.title
    except RecipeNotFoundException as e:
        logger.error(e)
        raise e
    except FavoriteAlreadyExistsException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e

def view_fav(user_id: int, title: str, category: str, username: str, sort_by: str, page: int, page_size: int, db: Session):
    try:
        query = db.query(Recipe).join(Favorite, Favorite.recipe_id == Recipe.id).join(User, Recipe.username == User.username)

        # Filter by user_id
        query = query.filter(Favorite.user_id == user_id)

        if title:
            query = query.filter(Recipe.title.ilike(f"%{title}%"))
        if category:
            if category.capitalize( ) not in categories:
                raise WrongCategoryException( )
            query = query.filter(Recipe.category == category.capitalize( ))
        if username:
            query = query.filter(User.username.ilike(f"%{username}%"))

        if sort_by == "date":
            query = query.order_by(desc(Recipe.created_at))
        elif sort_by == "date_asc":
            query = query.order_by(asc(Recipe.created_at))

        total_results = query.count( )
        results = query.offset((page - 1) * page_size).limit(page_size).all( )

        results = [RecipeFavoriteSearchDTO(
            id=recipe.id,
            title=recipe.title,
            username=recipe.username,
            category=recipe.category,
            ingredients=recipe.ingredients,
            steps=recipe.steps,
            photo=recipe.photo,
            avg_rating=get_avg_rating(recipe.id, db),
            created_at=recipe.created_at
        ) for recipe in results]

        return {
            "total": total_results,
            "page": page,
            "page_size": page_size,
            "results": results
        }
    except WrongCategoryException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Error occurred while searching for recipes")
