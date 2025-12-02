import asyncio
import json
from aiokafka import AIOKafkaConsumer
from motor.motor_asyncio import AsyncIOMotorClient


class AnalyticsWorkerAsync:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            'book_views',
            bootstrap_servers='kafka:9092',
            group_id='analytics',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
        )

        self.client_mongo = AsyncIOMotorClient(
            'mongodb://admin:admin123@mongo_db:27017/?authSource=admin'
        )
        self.db = self.client_mongo['analytics']
        self.collection = self.db['events_book']

    async def start_consume_loop(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                raw_msg = msg.value.decode()

                if not raw_msg:
                    continue
                data = json.loads(raw_msg)
                await self.collection.insert_one(data)
                print(f'Добавили в базу: {data}')
                print(f'Партиция: {msg.partition}')
                await self.consumer.commit()
        finally:
            await self.consumer.stop()


async def main():
    worker = AnalyticsWorkerAsync()
    await worker.start_consume_loop()


if __name__ == '__main__':
    asyncio.run(main())
