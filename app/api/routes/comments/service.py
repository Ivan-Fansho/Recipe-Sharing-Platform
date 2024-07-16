from datetime import date

from app.api.routes.comments.dtos import CreateCommentDTO
from app.api.utils.custom_errors import RecipeNotFoundException
from app.core.models import Comment, Recipe
import logging

logger = logging.getLogger(__name__)
def create(user_id: int, comment: CreateCommentDTO, db):
    try:
        recipe = db.query(Recipe).filter(Recipe.id == comment.recipe_id).first()
        if not recipe:
            raise RecipeNotFoundException()
        new_comment = Comment(user_id=user_id, recipe_id=recipe.id, comment=comment.comment)
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except RecipeNotFoundException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e