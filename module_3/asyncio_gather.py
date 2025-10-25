import asyncio
import time


async def a_sleep(x):
    await asyncio.sleep(x)
    return x


async def main():
    res = await asyncio.gather(a_sleep(1), a_sleep(2), a_sleep(3))
    return res

if __name__ == "__main__":
    start_time = time.time()
    print(asyncio.run(main()))
    finish_time = time.time()
    print(finish_time - start_time)
