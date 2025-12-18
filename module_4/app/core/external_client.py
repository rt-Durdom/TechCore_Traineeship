import httpx
from module_4.app.core.circuit_breaker import book_service_breaker


async def fetch_external(url: str) -> httpx.Response:
    async with httpx.AsyncClient(timeout=5.0) as client:
        return await book_service_breaker.call_async(client.get, url)
