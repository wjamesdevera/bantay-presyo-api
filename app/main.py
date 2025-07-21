from fastapi import FastAPI
from .routers import categories
from app.models import base
from app.database import engine

app = FastAPI()

app.include_router(categories.router)


base.BaseModel.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"API Name": "Bantay Presyo API"}
