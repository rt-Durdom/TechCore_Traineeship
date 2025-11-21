import pytest
from unittest.mock import AsyncMock
import httpx
import pybreaker
from async_core.AsyncClient_service import AuthorService


@pytest.mark.asyncio
async def test_circuit_breaker_trips_after_failures(mocker):
    service = AuthorService(base_url='http://example.com')

    mocker.patch.object(service.client, 'get', AsyncMock(side_effect=httpx.RequestError('Что-то пошло не так')))
    for _ in range(5):
        with pytest.raises(Exception):
            await service.get_data()

    with pytest.raises(pybreaker.CircuitBreakerError):
        await service.get_data()
