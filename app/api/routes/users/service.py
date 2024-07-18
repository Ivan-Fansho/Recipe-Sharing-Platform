import logging
from sqlalchemy.orm import Session
from app.core.db_dependency import get_db
from app.core.models import User
from .dtos import UserDTO, UpdateUserDTO, ShowUserDTO
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from ...utils import custom_emails

from ...authentication.authentication_service import hash_pass

logger = logging.getLogger(__name__)




def create(user: UserDTO, db: Session):
    try:
        hashed_password = hash_pass(user.password)

        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        custom_emails.registration_email_sender(new_user)
        custom_emails.registration_email_sender_to_admin(new_user)
        return new_user
    except IntegrityError as e:
        logger.error(f"Integrity error during user creation: {e}")
        db.rollback()
        if "phone_number" in str(e.orig):
            raise HTTPException(
                status_code=400, detail="Phone number already exists"
            ) from e
        elif "username" in str(e.orig):
            raise HTTPException(
                status_code=400, detail="Username already exists"
            ) from e
        elif "email" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already exists") from e
        else:
            raise HTTPException(
                status_code=400, detail="Could not complete registration"
            ) from e
    except Exception as e:
        # db.rollback()
        logger.error(f"Unexpected error during user creation: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error"
        ) from e

def update_user(id, update_info: UpdateUserDTO, db: Session = Depends(get_db)):
    try:
        # Retrieve the existing user
        user = db.query(User).filter_by(id=id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the user's attributes
        if update_info.password:
            user.password = hash_pass(update_info.password)
            custom_emails.update_password_email_sender(user, update_info.password, user.email)
        if update_info.email:
            user.email = update_info.email
        if update_info.bio:
            user.bio = update_info.bio
        if update_info.photo:
            user.photo = update_info.photo


        # Commit the changes to the database
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError as e:
        logger.error(f"Integrity error during user creation: {e}")
        db.rollback()
        if "username" in str(e.orig):
            raise HTTPException(
                status_code=400, detail="Username already exists"
            ) from e
        elif "email" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already exists") from e
        else:
            raise HTTPException(
                status_code=400, detail="Could not complete update"
            ) from e

def get_current_user(user_id, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ShowUserDTO(id=user.id,username=user.username, email=user.email, bio=user.bio, profile_pic=user.profile_picture)