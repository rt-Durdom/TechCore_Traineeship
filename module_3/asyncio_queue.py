import asyncio
from asyncio import Queue


async def producer(q):
    await q.put(1)
    return 1


async def consumer(q):
    res = await q.get()
    return res


async def main():
    q = Queue()
    res = await asyncio.gather(producer(q), consumer(q))
    return res

if __name__ == "__main__":
    print(asyncio.run(main()))
    # [1, 1]
