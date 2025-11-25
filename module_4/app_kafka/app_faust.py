import faust

app = faust.App('book-views', broker='kafka://kafka1:9092')

book_topic = app.topic('book_views')


@app.agent(book_topic)
def count_views(stream):
    count = 0
    for event in stream:
        count += 1
        print(f'Заглянули посмотреть, раз: {count}')
    