from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException

from .schemas.books import BookSchema
from .core.db import get_db_session, Session
from .api.routers import api_router

app = FastAPI()

app.include_router(api_router)