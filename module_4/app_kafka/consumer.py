from confluent_kafka import Consumer


class AnalyticsWorker:
    def __init__(self, ):
        self.consumer = Consumer({
            'bootstrap.servers': 'kafka1:9092',
            'group.id': 'analytics',
            'auto.offset.reset': 'earliest'
        })
    
    def start_consumer(self):
        self.consumer.subscribe(['event_books'])


consumer = AnalyticsWorker()
