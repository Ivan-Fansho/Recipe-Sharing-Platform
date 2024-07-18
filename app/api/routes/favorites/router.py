from fastapi import APIRouter, Depends, Query, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api.routes.favorites import service
from app.api.authentication.authentication_service import get_current_user
from app.api.routes.ratings.dtos import GiveRatingDTO
from app.api.routes.users.dtos import UserViewDTO
from app.api.utils.check_if_restricted import check_if_user_is_restricted
from app.core.db_dependency import get_db

favorites_router = APIRouter(prefix="/favorites", tags=["Favorites"])

@favorites_router.post("/add_favorite")
def add_favorite(current_user: UserViewDTO = Depends(get_current_user),
                 recipe_id: int = Query(..., gt=0),
                 db: Session = Depends(get_db)):
    check_if_user_is_restricted(current_user.id, db)
    result = service.add_fav(current_user.id, recipe_id, db)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": f"Added {result} to your favorites"})


@favorites_router.delete("/remove_favorite")
def remove_favorite(current_user: UserViewDTO = Depends(get_current_user),
                    recipe_id: int = Query(..., gt=0),
                    db: Session = Depends(get_db)):
    check_if_user_is_restricted(current_user.id, db)
    result = service.remove_fav(current_user.id, recipe_id, db)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Removed {result} to your favorites"})

@favorites_router.get("/view_favorites")
def view_favorites(current_user: UserViewDTO = Depends(get_current_user),
    title: str = Query(None, description="Search by title"),
    category: str = Query(None, description="Search by category"),
    username: str = Query(None, description="Search by username"),
    sort_by: str = Query(None, description="Sort by date 'asc' or 'desc'"),
    page: int = Query(1, description="Page number for pagination", ge=1),
    page_size: int = Query(10, description="Number of results per page", ge=1),
    db: Session = Depends(get_db)
):
    check_if_user_is_restricted(current_user.id, db)
    favorites = service.view_fav(
        current_user.id,
        title=title,
        category=category,
        username=username,
        sort_by=sort_by,
        page=page,
        page_size=page_size,
        db=db
    )

    return favorites