import redis
import os

from motor.motor_asyncio import AsyncIOMotorClient
from module_4.app.crud.mongo_crud import ReviewService
from dotenv import load_dotenv


redis_util = redis.asyncio.Redis(host='redis_db', port=6379, db=0, decode_responses=True)


async def get_review_service() -> ReviewService:
    username = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'admin')
    password = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'admin123')
    client = AsyncIOMotorClient(
        f"mongodb://{username}:{password}@mongo_db:27017/"
    )
    return ReviewService(client)


async def get_mongo_client() -> AsyncIOMotorClient:
    username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
    password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    client = AsyncIOMotorClient(
        f"mongodb://{username}:{password}@mongo_db:27017/"
    )
    try:
        yield client
    finally:
        client.close()

# class Session:
#     def __init__(self):
#         self.conntect = "connection"

#     def responce(self):
#         return "Результат запроса"

#     def close(self):
#         print("Закрываем соединение...")


# def get_db_session():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()
