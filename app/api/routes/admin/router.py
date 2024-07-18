from fastapi import APIRouter, Depends, Query, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api.routes.admin import service
from app.api.authentication.authentication_service import get_current_user
from app.api.routes.users.dtos import UserViewDTO
from app.api.utils.check_if_restricted import check_if_user_is_admin
from app.core.db_dependency import get_db


admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.get("/users")
def get_users(current_user: UserViewDTO = Depends(get_current_user),
              username: str = Query(None, description="Search by username"),
              email: str = Query(None, description="Search by email"),
              is_restricted: str = Query(None, description="Search restricted ot non restricted 'yes' or 'no'"),
              page: int = Query(1, description="Page number for pagination", ge=1),
              page_size: int = Query(10, description="Number of results per page", ge=1),
              db: Session = Depends(get_db)):

    check_if_user_is_admin(current_user.id, db)

    users = service.search_user(username, email,is_restricted, page, page_size, db)

    return users

@admin_router.put("/restrict")
def restrict(current_user: UserViewDTO = Depends(get_current_user),
             user_id: int = Query(None, description="User id"),
             restriction: str = Query(None, description="Restriction 'block' or 'unblock'"),
             db: Session = Depends(get_db)):
    check_if_user_is_admin(current_user.id, db)

    result = service.restrict_user(user_id, restriction, db)

    return JSONResponse(status_code=200, content={"message": f"User: {result} was {restriction}ed"})

@admin_router.get("/recipes/")
def get_recipes(current_user: UserViewDTO = Depends(get_current_user),):
    pass