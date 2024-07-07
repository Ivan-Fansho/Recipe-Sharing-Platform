from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends, Body, Response, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.authentication.authentication_service import ACCESS_TOKEN_EXPIRE_MINUTES, create_token, \
    authenticate_user, get_current_user
from app.api.routes.recipes import service
from app.api.routes.recipes.dtos import RecipeDTO, RecipeUpdateDTO
from app.api.routes.users.dtos import UserViewDTO
from app.api.utils.custom_errors import RecipeNotFoundException
from app.core.db_dependency import get_db


recipe_router = APIRouter(prefix="/recipes", tags=["Recipes"])

@recipe_router.post("/create")
def create_recipe(current_user: UserViewDTO = Depends(get_current_user),
        recipe: RecipeDTO = Body(..., example={
        "title": "Peperoni Pizza",
        "ingredients": "Dough, tomato souse, mozzarella, peperoni",
        "steps": "1.stretch the dough 2.put on the tomato souse, 3.spread the mozzarella 4.put on the peperoni",
        "category": "pizzas",
        "photo": "photo.jpeg/photo_path",
    }),
    db: Session = Depends(get_db)
):
    recipe = service.create(recipe, current_user, db)
    if recipe:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="New recipe created")


@recipe_router.post("/update")
def update_recipe(current_user: UserViewDTO = Depends(get_current_user),
        recipe_id: int = Query(description="Recipe ID"),
        recipe: RecipeUpdateDTO = Body(..., example={
        "title": "Peperoni Pizza",
        "ingredients": "Dough, tomato souse, mozzarella, peperoni",
        "steps": "1.stretch the dough 2.put on the tomato souse, 3.spread the mozzarella 4.put on the peperoni",
        "category": "pizzas",
        "photo": "photo.jpeg/photo_path",
    }),
    db: Session = Depends(get_db)
):
    service.update(recipe_id, recipe, current_user, db)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="recipe updated")


# @recipe_router.get("/search")
# def search_recipes_endpoint(
#     title: str = Query(None, description="Search by title"),
#     category: str = Query(None, description="Search by category"),
#     username: str = Query(None, description="Search by username"),
#     sort_by: str = Query(None, description="Sort by 'date' or 'ratings'"),
#     page: int = Query(1, description="Page number for pagination", ge=1),
#     page_size: int = Query(10, description="Number of results per page", ge=1),
#     db: Session = Depends(get_db)
# ):
#     try:
#         results = service.search_recipes(
#             title=title,
#             category=category,
#             username=username,
#             sort_by=sort_by,
#             page=page,
#             page_size=page_size,
#             db=db
#         )
#         return results
#     except RecipeNotFoundException as e:
#         raise HTTPException(status_code=404, detail=str(e))