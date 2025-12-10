from fastapi import APIRouter

from module_4.app.api.endpoints.books import router as books_router
from module_4.app.api.endpoints.orders import cel_router

api_router = APIRouter()

api_router.include_router(
    books_router, prefix='/api/books', tags=['books'])
api_router.include_router(
    cel_router, prefix='/celery', tags=['orders'])
