import asyncio
import random


async def a_sleep(lock):
    x = random.randint(1, 10)
    async with lock:
        await asyncio.sleep(x)
        print(f'Завершено задача на {x} секунд')


async def main():
    lock = asyncio.Lock()
    tasks = [a_sleep(lock) for _ in range(1, 11)]
    await asyncio.gather(*tasks)
    return 'Завершены все задачи'


if __name__ == "__main__":
    print(asyncio.run(main()))
