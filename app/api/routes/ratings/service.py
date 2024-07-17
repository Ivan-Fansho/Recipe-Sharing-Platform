from app.api.utils.custom_errors import RecipeNotFoundException, RatingAlreadyExistsException
from app.core.models import Recipe, Rating
import logging

logger = logging.getLogger(__name__)

def give(user_id, rating, db):
    try:
        recipe = db.query(Recipe).filter(Recipe.id == rating.recipe_id).first()
        if not recipe:
            raise RecipeNotFoundException()
        exists_rating = db.query(Rating).filter(Rating.recipe_id == rating.recipe_id, Rating.user_id == user_id).first()
        if exists_rating:
            raise RatingAlreadyExistsException()
        new_rating = Rating(recipe_id=recipe.id, user_id=user_id, rating=rating.rating)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return (rating.rating, recipe.title)
    except RecipeNotFoundException as e:
        logger.error(e)
        raise e
    except RatingAlreadyExistsException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e