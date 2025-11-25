from confluent_kafka import Producer


config_kafka = {'bootstrap.servers': 'kafka1:9092',
                'client.id': 'test-producer-1'}

producer = Producer(config_kafka)


def acked(err, msg):
    if err is not None:
        print('Ошибка в получении: %s: %s' % (str(msg), str(err)))
    else:
        print('Доставлено в кафка: %s' % (str(msg)))
