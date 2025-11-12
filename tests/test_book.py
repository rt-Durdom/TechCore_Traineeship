import pytest
import httpx
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from module_4.app.models.async_crud import CRUDAsyncBase
from module_4.app.models import Book
from .conftest import fast_test_client
from module_4.app.core.db import get_db_session
from module_4.app.main import app


#pytest-asyncio
@pytest.mark.asyncio
async def test_mock_get_book(mocker):
    book_service = CRUDAsyncBase(Book)
    test_book = Book(id=5, title='Тест', author='Пушукин', year=1812)
    mock_session = mocker.AsyncMock(spec=AsyncSession)
    mocket_data = mocker.patch.object(
        book_service,
        'get_obj_by_id',
        AsyncMock(return_value=test_book)
    )
    result = await book_service.get_obj_by_id(5, mock_session)
    assert result.id == 5
    assert result.title == 'Тест'
    assert result.author == 'Пушукин'
    assert result.year == 1812
    assert test_book == result

    mocket_data.assert_called_once_with(5, mock_session)


def test_get_book_endpoint():
    response = fast_test_client.get('/books')
    assert response.status_code == 200


def test_get_book_endpoint_sesion():
    mock_session = AsyncMock(spec=AsyncSession)
    app.dependency_overrides[get_db_session] = lambda: mock_session
    try:
        response = fast_test_client.get('/books')
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_post_book_pydantic():
    response = fast_test_client.post(
        '/books/books',
        json={'title': 123, 'author': "Пушукин", 'year': 1812}
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_async_get_book():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get('/books')

    assert response.status_code == 200
