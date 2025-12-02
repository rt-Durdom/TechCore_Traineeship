from .producer import producer, acked


def send_event_book(book_id, book_title):
    producer.produce(
        topic='book_views',
        key=str(book_id),
        value=f'Посмотрели книгу: {book_title}',
        callback=acked
    )
    producer.poll(0)
