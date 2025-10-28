from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from app.schemas.books import BookSchema

app = FastAPI()

book_dict = dict()
id = 1


@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.post('/books')
def create_book(book: BookSchema):
    if book_dict[id]:
        id += 1
        book_dict[id] = book
    book_dict[id] = book
    return f'Под номером {id} книга {book.title} создана'

@app.get('/books/{book_id}')
def read_book(book_id: int):
    if book_id not in book_dict:
        raise HTTPException(status_code=404, detail='Книга не найдена')
    return f'Книга {book_dict[book_id].title}'
