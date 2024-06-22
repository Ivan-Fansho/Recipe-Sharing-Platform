import os
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse, JSONResponse


user_router = APIRouter(prefix="/users", tags=["Users"])







