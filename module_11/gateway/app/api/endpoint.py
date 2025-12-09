import asyncio
import os
import httpx
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from gateway.app.api.auth_jwt import verify_jwt


BOOK_SERVICE_URL = os.getenv('BOOK_SERVICE_URL', 'http://book-service:8000')
REVIEW_SERVICE_URL = os.getenv("REVIEW_SERVICE_URL", "http://book-service:8000")


router_gateway = APIRouter()


class BookCreate(BaseModel):
    title: str
    year: int



@router_gateway.get('/books')
async def books():
    return {'status': 'ok'}


@router_gateway.get('/{book_id}')
async def proxy_book(book_id: int, user=Depends(verify_jwt)):
    url = f'{BOOK_SERVICE_URL}/api/books/{book_id}'
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            responce = await client.get(url)
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f'ОШибка: {e}'
        )

    return responce.json() if responce.is_success else HTTPException(
        status_code=responce.status_code, detail=responce.text
    )


@router_gateway.post('')
async def create_book(book: BookCreate, user=Depends(verify_jwt)):
    url = f'{BOOK_SERVICE_URL}/api/books/'

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=book.dict())
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f'Gateway error: {str(e)}'
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()


@router_gateway.get('/details/{id}')
async def agregated(id: int, user=Depends(verify_jwt)):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            book = client.get(f'{BOOK_SERVICE_URL}/api/books/{id}')
            reviews = client.get(f'{REVIEW_SERVICE_URL}/api/products/{id}/details')
            book_resp, reviews_resp = await asyncio.gather(book, reviews)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f'Ошибка сервиса: {e}')

    if not book_resp.is_success:
        raise HTTPException(status_code=book_resp.status_code, detail=book_resp.text)
    if not reviews_resp.is_success:
        raise HTTPException(status_code=reviews_resp.status_code, detail=reviews_resp.text)

    return {
        "book": book_resp.json(),
        "reviews": reviews_resp.json()['Отзывс'],
    }
