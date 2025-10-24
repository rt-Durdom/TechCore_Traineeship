import asyncio


async def stream_data():
    for i in range(1, 10):
        await asyncio.sleep(1)
        yield i


async def main():
    async for info in stream_data():
        print(info)


if __name__ == "__main__":
    asyncio.run(main())

    # 1
    # 2
    # 3 ... 9
