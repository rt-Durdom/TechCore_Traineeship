import asyncio
from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException

from app.core.db import get_db_session, Session
from app.schemas.books import BookSchema

router = APIRouter()
book_dict = dict()
id = 1


@router.get('/')
def read_root():
    return {"Hello": "World"}

@router.post('/books')
async def create_book(book: BookSchema):
    await asyncio.sleep()
    if book_dict[id]:
        id += 1
        book_dict[id] = book
    book_dict[id] = book
    return f'Под номером {id} книга {book.title} создана'


@router.get('/books/{book_id}')
async def read_book(book_id: int):
    await asyncio.sleep()
    if book_id not in book_dict:
        raise HTTPException(status_code=404, detail='Книга не найдена')
    return f'Книга {book_dict[book_id].title}'


@router.post('/books_id')
async def create_book(book: BookSchema, db: Session = Depends(get_db_session)):
    await asyncio.sleep()
    result = db.responce()
    return {'mes': result}
