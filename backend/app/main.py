import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from api.routes.users.router import user_router
from backend.app.core import models
from backend.app.core.database import engine
from backend.app.core.models import Base
import os
from fastapi.openapi.docs import get_swagger_ui_html

load_dotenv()
app = FastAPI()


from api.routes.users.router import user_router
app.include_router(user_router)


app.include_router(user_router)
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app="main:app", host="127.0.0.1", port=8001, reload=True)
