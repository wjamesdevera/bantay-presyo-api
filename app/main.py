from typing import Annotated
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .models import create_db_and_tables
from .api import categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


# Code below omitted 👇
app.include_router(categories.router)


@app.get("/")
async def root():
    return {"API Name": "Bantay Presyo API"}
