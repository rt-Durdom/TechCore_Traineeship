import sys

from confluent_kafka import Consumer
from confluent_kafka.cimpl import KafkaError
from confluent_kafka.error import KafkaException


class AnalyticsWorker:
    def __init__(self, ):
        self.consumer = Consumer({
            'bootstrap.servers': 'kafka1:9092',
            'group.id': 'analytics',
            'auto.offset.reset': 'earliest'
        })

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
                    self.consumer.commit(asynchronous=True)

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()


consumer = AnalyticsWorker()
