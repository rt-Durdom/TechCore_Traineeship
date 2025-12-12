import asyncio
import module_4.app_kafka.opentel_config_kafka
import json
from aiokafka import AIOKafkaConsumer
from motor.motor_asyncio import AsyncIOMotorClient
from opentelemetry import trace


class AnalyticsWorkerAsync:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            'book_views',
            bootstrap_servers='kafka1:9092',
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
        tracer = trace.get_tracer(__name__)
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                # для Kafka
                with tracer.start_as_current_span('kafka.receive') as kafka_span:
                    kafka_span.set_attribute('messaging.system', 'kafka')
                    kafka_span.set_attribute('messaging.destination', msg.topic)
                    kafka_span.set_attribute('messaging.kafka.partition', msg.partition)
                    raw_msg = msg.value.decode()
                    if not raw_msg:
                        continue

                    # для MongoDB
                    with tracer.start_as_current_span('mongodb.insert') as mongo_span:
                        mongo_span.set_attribute('db.system', 'mongodb')
                        mongo_span.set_attribute('db.name', 'analytics')
                        mongo_span.set_attribute('db.collection', 'events_book')
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
else:
    asyncio.run(main())
