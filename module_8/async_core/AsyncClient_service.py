import asyncio
import aiohttp
import backoff
import httpx
import pybreaker


async def get_author_service():
    """
    Dependency для AuthorService
    """
    async with AuthorService() as av_service:
        yield av_service


class AuthorService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        self.circuit_breaker = pybreaker.CircuitBreaker(fail_max=5)
        self.semaphore = asyncio.Semaphore(5)


    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    async def get_data(self, id: int):

        try:
            async with self.semaphore:
                task1 = await asyncio.wait_for(
                    self.circuit_breaker.call_async(
                        self.client.get, f'{self.base_url}/authors/{id}'
                    ), timeout=2.0
                )
                task2 = await asyncio.wait_for(
                    self.circuit_breaker.call_async(
                        self.client.get, f'{self.base_url}/api/reviews/{id}'
                    ), timeout=2.0
                )
                responses = await asyncio.gather(task1, task2)

                return responses
        except asyncio.TimeoutError as te:
            raise TimeoutError(f'Время ожидания истекл. Ошибка {te}')
        except pybreaker.CircuitBreakerError:
            return 'Default'
        except Exception as e:
            raise Exception(f'Что-то пошло не так {e}')
        finally:
            await self.client.aclose()

    async def get_aiohttp_client(self, id: int):
        try:
            async with aiohttp.ClientSession() as aio_client:
                response = await asyncio.wait_for(
                        aio_client.get(f'{self.base_url}/authors/{id}'),
                        timeout=2.0
                )
                return response
        except asyncio.TimeoutError as te:
            raise TimeoutError(f'Время ожидания истекл. Ошибка {te}')
        except Exception as e:
            raise Exception(f'Что-то пошло не так {e}')
