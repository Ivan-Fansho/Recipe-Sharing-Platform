import logging
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api.routes.comments.dtos import CommentShowDTO
from app.api.routes.recipes.dtos import RecipeDTO, RecipeUpdateDTO, RecipeShowDTO
from app.api.routes.users.dtos import UserViewDTO
from app.api.utils.categories import categories
from app.api.utils.custom_errors import WrongCategoryException, WrongUserException, RecipeNotFoundException
from app.core.models import Recipe, User

logger = logging.getLogger(__name__)

def create(recipe: RecipeDTO, user: UserViewDTO, db: Session):
    try:
        if recipe.category not in categories:
            raise WrongCategoryException()

        new_recipe = Recipe(username=user.username, title=recipe.title,
                            ingredients=recipe.ingredients, steps=recipe.steps,
                            category=recipe.category, photo=recipe.photo)

        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    except WrongCategoryException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Recipe could not be created")

def update(recipe_id: int, update_info: RecipeUpdateDTO, user: UserViewDTO, db: Session):
    try:
        recipe = db.query(Recipe).filter_by(id=recipe_id).first()
        if not recipe:
            raise RecipeNotFoundException()
        if recipe.username != user.username:
            raise WrongUserException()

        if update_info.title:
            recipe.title = update_info.title
        if update_info.ingredients:
            recipe.ingredients = update_info.ingredients
        if update_info.steps:
            recipe.steps = update_info.steps
        if update_info.category:
            if update_info.category.capitalize() not in categories:
                raise WrongCategoryException()
            recipe.category = update_info.category
        if update_info.photo:
            recipe.photo = update_info.photo

        db.commit()
        db.refresh(recipe)
    except RecipeNotFoundException as e:
        logger.error(e)
        raise e
    except WrongCategoryException as e:
        logger.error(e)
        raise e
    except WrongUserException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Recipe could not be updated")

def search_recipes(title: str, category: str, username: str, sort_by: str, page: int, page_size: int, db: Session):
    try:
        query = db.query(Recipe)

        if title:
            query = query.filter(Recipe.title.ilike(f"%{title}%"))
        if category:
            if category.capitalize() not in categories:
                raise WrongCategoryException()
            query = query.filter(Recipe.category == category.capitalize())
        if username:
            query = query.filter(Recipe.username.ilike(f"%{username}%"))

        if sort_by == "date":
            query = query.order_by(desc(Recipe.created_at))
        # Uncomment if you have a ratings field
        # elif sort_by == "ratings":
        #     query = query.order_by(desc(Recipe.ratings))

        total_results = query.count()
        results = query.offset((page - 1) * page_size).limit(page_size).all()

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

def get_username_by_id(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    return user.username

def map_recipe_to_dto(recipe, db: Session):
    return RecipeShowDTO(
        title=recipe.title,
        category=recipe.category,
        ingredients=recipe.ingredients,
        steps=recipe.steps,
        photo=recipe.photo,
        created_at=recipe.created_at,
        comments=[CommentShowDTO(
            username=get_username_by_id(comment.user_id, db),
            created_at=comment.created_at,
            comment=comment.comment
        ) for comment in recipe.comments]
    )

def view(id, db):
    try:
        db_recipe = db.query(Recipe).filter_by(id=id).first()
        if not db_recipe:
            raise RecipeNotFoundException()
        return map_recipe_to_dto(db_recipe, db)
    except RecipeNotFoundException as e:
        logger.error(e)
        raise e