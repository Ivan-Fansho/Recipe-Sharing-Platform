from sqlalchemy.orm import Session

from app.api.utils.custom_errors import BlockedUserException, NotAdminUserException
from app.core.models import User


def check_if_user_is_restricted(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user.is_restricted is True:
        raise BlockedUserException()

def check_if_user_is_admin(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user.is_admin is False:
        raise NotAdminUserException()