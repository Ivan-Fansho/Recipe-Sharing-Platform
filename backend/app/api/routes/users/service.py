import logging
from sqlalchemy.orm import Session

from backend.app.core.db_dependency import get_db
from backend.app.core.models import User
from .dtos import UserDTO, UpdateUserDTO, UserShowDTO, UserFromSearchDTO, ContactDTO
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, Depends
from mailjet_rest import Client

from ...authentication.authentication_service import hash_pass

logger = logging.getLogger(__name__)
def registration_email_sender(user):
    api_key = 'cdcb4ffb9ac758e8750f5cf5bf07ac9f'
    api_secret = '8ec6183bbee615d0d62b2c72bee814c4'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "kis.team.telerik@gmail.com",
                    "Name": "MyPyWallet"
                },
                "To": [
                    {
                        "Email": f"{user.email}",
                        "Name": f"{user.fullname}"
                    }
                ],
                "Subject": f"Registration to PyMyWallet",
                "HTMLPart": f"<h3>Thanks for registering, please wait for your registration to be confirmed.</h3><br />May the delivery force be with you!",
                "CustomID": f"UserID: {user.id}"
            }
        ]
    }
    mailjet.send.create(data=data)

def email_sender(user):
    api_key = 'cdcb4ffb9ac758e8750f5cf5bf07ac9f'
    api_secret = '8ec6183bbee615d0d62b2c72bee814c4'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "kis.team.telerik@gmail.com",
                    "Name": "MyPyWallet Admin"
                },
                "To": [
                    {
                        "Email": "kis.team.telerik@gmail.com",
                        "Name": "Kis"
                    }
                ],
                "Subject": f"New Registration UserID:{user.id}",
                "HTMLPart": f"<h3>New user {user.username} with id:{user.id} waits for confirmation</h3><br />May the delivery force be with you!",
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    mailjet.send.create(data=data)



def create(user: UserDTO, db: Session):
    try:
        hashed_password = hash_pass(user.password)

        new_user = User(
            username=user.username,
            password=hashed_password,
            email=user.email,
            phone_number=user.phone_number,
            fullname=user.fullname
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.commit()
        email_sender(new_user)
        registration_email_sender(new_user)
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
        db.rollback()
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
        if update_info.email:
            user.email = update_info.email
        if update_info.phone_number:
            user.phone_number = update_info.phone_number
        if update_info.fullname:
            user.fullname = update_info.fullname

        # Commit the changes to the database
        db.commit()
        db.refresh(user)
        return user

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
                status_code=400, detail="Could not complete update"
            ) from e

