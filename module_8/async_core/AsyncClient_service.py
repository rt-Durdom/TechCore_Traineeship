import asyncio
import backoff
import httpx
import pybreaker


class AuthorService:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        self.circuit_breaker = pybreaker.CircuitBreaker(fail_max=5)

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
    async def get_data(self):

        try:
            response = await asyncio.wait_for(
                self.circuit_breaker.async_call(
                    self.client.get(self.base_url), timeout=2.0
                )
            )
            return response
        except asyncio.TimeoutError as te:
            raise TimeoutError(f'Время ожидания истекл. Ошибка {te}')
        except pybreaker.CircuitBreakerError as cbe:
            raise Exception(f'CircuitBreakerError": {cbe}')
        except Exception as e:
            raise Exception(f'Что-то пошло не так {e}')
        finally:
            await self.client.aclose()
