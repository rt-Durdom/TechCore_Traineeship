import json
from .producer import producer, acked


def send_event_book(book_id, book_title):
    event_data = {
        'book_id': book_id,
        'book_title': book_title,
        'event': 'book_viewed'
    }
    producer.produce(
        topic='book_views',
        key=str(book_id),
        value=json.dumps(event_data),
        callback=acked
    )
    producer.poll(0)
