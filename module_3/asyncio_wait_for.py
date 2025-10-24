import asyncio


async def eternity():
    await asyncio.sleep(5)
    print('Програма сна заверешна!')


async def main():
    try:
        await asyncio.wait_for(eternity(), timeout=2)
    except TimeoutError:
        print('Досросчно завершили сон!')


if __name__ == "__main__":
    asyncio.run(main())
