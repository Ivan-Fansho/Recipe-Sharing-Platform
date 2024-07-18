from fastapi import APIRouter, Depends, Query, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.api.routes.ratings import service
from app.api.authentication.authentication_service import get_current_user
from app.api.routes.ratings.dtos import GiveRatingDTO
from app.api.routes.users.dtos import UserViewDTO
from app.api.utils.check_if_restricted import check_if_user_is_restricted
from app.core.db_dependency import get_db
from app.core.models import Rating

ratings_router = APIRouter(prefix="/ratings", tags=["Ratings"])

@ratings_router.post("/give")
async def give_ratings(current_user: UserViewDTO = Depends(get_current_user),
                       rating: GiveRatingDTO = Body(..., examples=[
                           {"recipe_id":1,
                            "rating": 5}]),
                       db: Session = Depends(get_db)):
    check_if_user_is_restricted(current_user.id, db)
    rating = service.give(current_user.id, rating, db)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": f"Successfully given rating of {rating[0]} stars to recipe {rating[1]}"})
