from sqlalchemy.orm import Session
from app.api.routes.admin.dtos import UserAdminViewDTO, CommentAdminShowDTO
from app.api.routes.recipes.service import get_username_by_id
from app.api.utils.custom_errors import InvalidRestrictionInputException, UserNotFoundException, \
    UserAlreadyBlockedException, UserAlreadyUnblockedException, InvalidRestrictionInputExceptionv2, \
    RecipeNotFoundException, CommentNotFoundException
from app.core.models import User, Comment, Recipe
import logging

logger = logging.getLogger(__name__)

def search_user(username: str, email: str,is_restricted:str, page: int, page_size: int, db: Session):
    try:
        users = db.query(User)
        if username:
            users = users.filter(User.username.ilike(f"%{username}%"))
        if email:
            users = users.filter(User.email.ilike(f"%{email}%"))
        if is_restricted:
            is_restricted_lower = is_restricted.lower( )
            if is_restricted_lower == "yes":
                users = users.filter(User.is_restricted == True)
            elif is_restricted_lower == "no":
                users = users.filter(User.is_restricted == False)
            else:
                raise InvalidRestrictionInputException()

        total_results = users.count()
        results = users.offset((page - 1) * page_size).limit(page_size).all( )

        results = [UserAdminViewDTO(id=user.id, username=user.username, email=user.email,
                                    profile_picture=user.profile_picture, bio=user.bio,
                                    is_restricted=user.is_restricted) for user in results]

        return {
            "total": total_results,
            "page": page,
            "page_size": page_size,
            "results": results
        }
    except InvalidRestrictionInputException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e


def restrict_user(user_id, restriction, db):
    try:
        restriction_lower = restriction.lower()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException()
        if restriction_lower == "block":
            if user.is_restricted == True:
                raise UserAlreadyBlockedException()
            user.is_restricted = True
            db.commit()
        elif restriction_lower == "unblock":
            if user.is_restricted == False:
                raise UserAlreadyUnblockedException()
            user.is_restricted = False
            db.commit()
        else:
            raise InvalidRestrictionInputExceptionv2()
        return user.username
    except UserNotFoundException as e:
        logger.error(e)
        raise e
    except UserAlreadyBlockedException as e:
        logger.error(e)
        raise e
    except UserAlreadyUnblockedException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e

def view_comments(user_id, recipe_id, page, page_size, db):
    try:
        comments = db.query(Comment)
        if user_id:
            user = db.query(User).filter(User.id == user_id).first( )
            if not user:
                raise UserNotFoundException( )
            comments = comments.filter(Comment.user_id == user_id)
        if recipe_id:
            recipe = db.query(Recipe).filter_by(id=recipe_id).first( )
            if not recipe:
                raise RecipeNotFoundException( )
            comments = comments.filter(Comment.recipe_id == recipe_id)

        total_results = comments.count( )
        results = comments.offset((page - 1) * page_size).limit(page_size).all( )

        results = [CommentAdminShowDTO(comment_id=comment.id,username=get_username_by_id(comment.user_id, db),
                recipe_id=comment.recipe_id,
                created_at=comment.created_at,
                comment=comment.comment
            ) for comment in results]

        return {
            "total": total_results,
            "page": page,
            "page_size": page_size,
            "results": results
        }
    except UserNotFoundException as e:
        logger.error(e)
        raise e
    except RecipeNotFoundException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e

def comment_delete(comment_id, db):
    try:
        comment = db.query(Comment).filter_by(id=comment_id).first()
        if not comment:
            raise CommentNotFoundException( )
        else:
            db.delete(comment)
            db.commit()
            return comment.id
    except CommentNotFoundException as e:
        logger.error(e)
        raise e
    except Exception as e:
        logger.error(e)
        raise e