import asyncio
import backoff
import httpx


class AuthorService:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    async def get_data(self):
        try:
            response = await asyncio.wait_for(await self.client.get(self.base_url), timeout=2.0)
            return response
        except asyncio.TimeoutError as e:
            raise TimeoutError(f'Время ожидания истекл. Ошибка {e}')
        except Exception as e:
            raise Exception(f'Что-то пошло не так {e}')
        finally:
            await self.client.aclose
