import httpx
import asyncio
import time


url = 'https://httpbin.org/get'


async def request_http(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.status_code


async def main():
    res = await asyncio.gather(*([request_http(url) for _ in range(100)]))
    return len(res)


if __name__ == "__main__":
    time_start = time.time()
    print(f'Количество запросов: {asyncio.run(main())}')
    time_finish = time.time()
    print(f'Время выполнения: {(time_finish - time_start):.2f} сек.')