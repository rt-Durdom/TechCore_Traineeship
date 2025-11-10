import pytest
from unittest.mock import AsyncMock

from module_4.app.models.async_crud import CRUDAsyncBase
from module_4.app.models import Book
from .conftest import fast_test_client


@pytest.mark.asyncio
async def test_mock_get_book(mocker):
    book_service = CRUDAsyncBase(Book)
    test_book = Book(id=5, title='Тест', author='Пушукин', year=1812)
    mock_session = mocker.Mock()
    mocket_data = mocker.patch.object(
        book_service,
        'get_obj_by_id',
        AsyncMock(return_value=test_book)
    )
    result = await book_service.get_obj_by_id(5, None)
    assert result.id == 5
    assert result.title == 'Тест'
    assert result.author == 'Пушукин'
    assert result.year == 1812
    assert test_book == result

    mocket_data.assert_called_once_with(5, mock_session)


def test_get_book_endpoint():
    response = fast_test_client.get('/books/books')
    assert response.status_code == 200
