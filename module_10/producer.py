from confluent_kafka import Producer


config_kafka = {'bootstrap.servers': 'localhost:9092',
                'client.id': 'test-producer-1'}

producer = Producer(config_kafka)


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


producer.produce('topic', key="key", value="value", callback=acked)


if __name__ == 'main':
    producer.poll(1)
    producer.flush()
