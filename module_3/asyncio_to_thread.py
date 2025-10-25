import asyncio
import time


def blocking_io():
    time.sleep(1)
    print('Сон завершен!')


async def main():
    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.sleep(5))

    print(f'Цикл событий завершен!')


if __name__ == "__main__":
    asyncio.run(main())
