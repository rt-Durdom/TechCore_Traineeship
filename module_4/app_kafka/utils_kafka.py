from .producer import producer, acked


def send_event_book(book_id, book_title):
    producer.produce(
        topic='event_books',
        key=str(book_id),
        value=f'Посмотрели книгу: {book_title}',
        callback=acked
    )
    producer.poll(0)
