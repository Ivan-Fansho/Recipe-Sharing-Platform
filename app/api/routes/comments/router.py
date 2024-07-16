from fastapi import APIRouter, Depends, Query, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api.routes.comments import service

from app.api.authentication.authentication_service import get_current_user
from app.api.routes.comments.dtos import CreateCommentDTO
from app.api.routes.users.dtos import UserViewDTO
from app.core.db_dependency import get_db

comment_router = APIRouter(prefix="/comments", tags=["Comments"])

@comment_router.post("/create")
def create_comment(current_user: UserViewDTO = Depends(get_current_user),
                   comment: CreateCommentDTO = Body(..., examples=[{"recipe_id": 1,
                                                                    "comment": "This was very helpful recipe, it turned out very delicious"}]),
                   db: Session = Depends(get_db)):
    service.create(current_user.id, comment, db)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Comment created"})