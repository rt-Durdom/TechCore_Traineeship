import redis
import asyncio


async def ping_redis():
    try:
        redis_ping = redis.asyncio.Redis(host='localhost', port=6379)
        print(f'Подключено к Redis {await redis_ping.ping()}')
    except redis.exceptions.ConnectionError:
        raise ConnectionError('Redis не подключился!')


async def main():
    return await ping_redis()

if __name__ == "__main__":
    asyncio.run(main())
