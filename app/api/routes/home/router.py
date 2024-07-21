from fastapi import APIRouter


home_router = APIRouter(tags=["Home"])


@home_router.get("/")
def home():
    return "Welcome to My Recipe Sharing App, there is no frontend but to check the endpoints go to /docs to see the FastApi swagger"