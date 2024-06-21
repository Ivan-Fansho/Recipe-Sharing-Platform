import os
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse, JSONResponse


user_router = APIRouter(prefix="/users", tags=["Users"])





@user_router.get("/")
def read_root():
    return {"message": "Welcome to my OAuth2 Implicit Flow Demo"}

