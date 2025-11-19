from fastapi import APIRouter

from app.api.endpoints.books import router as books_router
from app.api.endpoints.orders import cel_router

api_router = APIRouter()

api_router.include_router(
    books_router, prefix='/books', tags=['books'])
api_router.include_router(
    cel_router, prefix='/celery', tags=['orders'])
