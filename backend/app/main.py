import uvicorn
from fastapi import FastAPI

from backend.app.core import models
from backend.app.core.database import engine
from backend.app.core.models import Base

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app="main:app", host="127.0.0.1", port=8001, reload=True)