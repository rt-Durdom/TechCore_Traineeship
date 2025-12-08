import os
import httpx
from fastapi import APIRouter
from fastapi.exceptions import HTTPException


router_gateway = APIRouter()

@router_gateway.get('/books')
async def books():
    return {'status": "ok'}

BOOK_SERVICE_URL = os.getenv('http://book-service:8000')

@router_gateway.get('/books/{book_id}')
async def proxy_book(book_id: int):
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
