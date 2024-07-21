from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends, Body, Response, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.authentication.authentication_service import ACCESS_TOKEN_EXPIRE_MINUTES, create_token, \
    authenticate_user, get_current_user
from app.api.routes.users import service
from app.api.routes.users.dtos import UserViewDTO, UserDTO, UpdateUserDTO
from app.api.utils.check_if_restricted import check_if_user_is_restricted

from app.core.db_dependency import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])





@user_router.post("/register")
async def register_user(
    user: UserDTO = Body(..., examples=[{
        "username": "your_username",
        "password": "Password1!!",
        "email": "default@example.com"
    }]),
    db: Session = Depends(get_db)
):
    created_user = service.create(user, db)
    return {"message": f"User {created_user.username} created successfully."}


@user_router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"sub": user.username}, expires_delta=access_token_expires)

    # Set the token in a secure, HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Use True in production to ensure cookies are only sent over HTTPS
        samesite="lax"  # Adjust as needed for your use case
    )

    return {"message": "Login successful"}

@user_router.get("/me")
def read_users_me(current_user: UserViewDTO = Depends(get_current_user), db: Session = Depends(get_db)):
    check_if_user_is_restricted(current_user.id, db)

    return service.get_current_user(current_user.id, db)

@user_router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@user_router.put("/update")
def update_user(
    current_user: UserViewDTO = Depends(get_current_user),
        update_info: UpdateUserDTO = Body(
            ...,
            examples=[{
                "password": "Password1!",
                "email": "default@example.com",
                "photo_path": "photo.jpeg/photo_path",
                "bio": "This is the bio",

            }],
        ),
    db: Session = Depends(get_db),
):
    check_if_user_is_restricted(current_user.id, db)
    user = service.update_user(current_user.id, update_info, db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Profile updated successfully"
                 })

