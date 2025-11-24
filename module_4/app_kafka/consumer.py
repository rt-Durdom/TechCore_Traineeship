import sys
import json

from confluent_kafka import Consumer
from confluent_kafka.cimpl import KafkaError
from confluent_kafka.error import KafkaException
from pymongo import MongoClient


class AnalyticsWorker:
    def __init__(self, ):
        self.consumer = Consumer({
            'bootstrap.servers': 'kafka1:9092',
            'group.id': 'analytics',
            'auto.offset.reset': 'earliest'
        })
        self.client_mongo = MongoClient('mongodb://admin:admin123@mongo_db:27017/?authSource=admin')
        self.db = self.client_mongo['analytics']
        self.collection = self.db['events_book']


    def start_consume_loop(self):


        try:
            self.consumer.subscribe(['book_views'])
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                
                else:
                    print(msg)
                    data = json.loads(msg.value())
                    self.collection.insert_one(data)
                    print(f'Добавили в базу: {data}')
                    self.consumer.commit(asynchronous=True)

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()


consumer = AnalyticsWorker()

if __name__ == '__main__':
    consumer.start_consume_loop()
