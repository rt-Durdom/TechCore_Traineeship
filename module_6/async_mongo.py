from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv


load_dotenv('.env')


async def motor_goooo():
    try:
        username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
        password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
        client = AsyncIOMotorClient(
            f"mongodb://{username}:{password}@localhost:27017/"
        )
        await client.admin.command('ping')
        print('Подключено к MongoDB')
        return client
    except Exception as e:
        raise Exception(f'MongoDB не подключился! Ошибка: {e}')


async def main():
    await motor_goooo()


if __name__ == "__main__":
    asyncio.run(main())
