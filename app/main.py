from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from app.core import models
from app.core.database import engine
from app.core.db_dependency import get_db
from app.core.db_population import initialize_special_accounts
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


from api.routes.users.router import user_router
app.include_router(user_router)


app.include_router(user_router)
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app="main:app", host="127.0.0.1", port=8001, reload=True)
