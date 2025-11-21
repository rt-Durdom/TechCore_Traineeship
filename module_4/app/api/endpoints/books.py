import asyncio
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.books import BookSchema, BookDB, BookRead, AuthorShema
from app.models.async_crud import CRUDAsyncBase
from app.models.base import get_session
from app.models.books import Book
from module_8.async_core.AsyncClient_service import AuthorService, get_author_service

router = APIRouter()
# book_dict = dict()
# id = 1


# @router.get('/')
# def read_root():
#     return {"Hello": "World"}

@router.post('/', response_model=BookDB)
async def create_book(book: BookDB, session: AsyncSession = Depends(get_session)):
    new_book = await CRUDAsyncBase(Book).create(book, session)
    return new_book


@router.get('/', response_model=list[BookRead])
async def read_books(session: AsyncSession = Depends(get_session)):
    return await CRUDAsyncBase(Book).get(session)

@router.get('/{book_id}', response_model=BookRead)
async def read_book(
    book_id: int, 
    session: AsyncSession = Depends(get_session),
    service_author: AuthorService = Depends(get_author_service)
):
    book_info = await CRUDAsyncBase(Book).get_obj_by_id(book_id, session)
    author_info = await service_author.get_data(book_info.author_id)

    return BookDB(
        **jsonable_encoder(book_info),
        author=AuthorSchema(**author_info)
    )

@router.patch('/{book_id}', response_model=None)
async def update_book(book_id: int, book: BookSchema, session: AsyncSession = Depends(get_session)):
    data_book = await session.get(Book, book_id,)
    return await CRUDAsyncBase(Book).update(data_book, book, session)
