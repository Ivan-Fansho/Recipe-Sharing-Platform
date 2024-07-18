from sqlalchemy.orm import Session
from app.api.routes.admin.dtos import UserAdminViewDTO
from app.api.utils.custom_errors import InvalidRestrictionInputException, UserNotFoundException, \
    UserAlreadyBlockedException, UserAlreadyUnblockedException, InvalidRestrictionInputExceptionv2
from app.core.models import User
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