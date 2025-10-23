import asyncio


async def fetch_data():
    await asyncio.sleep(1)


async def main():
    await fetch_data()


asyncio.run(main()) 
