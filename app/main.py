import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core import models
from app.core.database import engine
from app.core.db_dependency import get_db
from app.core.db_population import initialize_special_accounts
from api.routes.users.router import user_router
from api.routes.recipes.router import recipe_router
from api.routes.comments.router import comment_router
from app.core.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize special accounts and categories during application startup
    db_gen = get_db()
    db = next(db_gen)
    try:
        initialize_special_accounts(db)
    finally:
        db_gen.close()

    yield  # Control is passed to the application

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(user_router)
app.include_router(recipe_router)
app.include_router(comment_router)

# Create all tables
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
