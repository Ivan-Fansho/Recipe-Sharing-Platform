from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends, Body, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.authentication.authentication_service import ACCESS_TOKEN_EXPIRE_MINUTES, create_token, \
    authenticate_user, get_current_user
from app.api.routes.recipes import service
from app.api.routes.recipes.dtos import RecipeDTO
from app.api.routes.users.dtos import UserViewDTO
from app.core.db_dependency import get_db


recipe_router = APIRouter(prefix="/recipes", tags=["Recipes"])

@recipe_router.post("create")
def create_recipe(current_user: UserViewDTO = Depends(get_current_user),
        recipe: RecipeDTO = Body(..., example={
        "title": "Peperoni Pizza",
        "ingredients": "Dough, tomato souse, mozzarella, peperoni",
        "steps": "1.stretch the dough 2.put on the tomato souse, 3.spread the mozzarella 4.pot on the peperoni",
        "category": "pizzas",
        "photo": "photo.jpeg/photo_path",
    }),
    db: Session = Depends(get_db)
):
    recipe = service.create(recipe, current_user, db)
    if recipe:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="New recipe created")