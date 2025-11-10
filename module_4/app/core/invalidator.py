from app.core.db import redis_util


class Invalidator:
    def __init__(self):
        self.pubsub = redis_util.pubsub()

    async def listen_for_invalidation(self):

        await self.pubsub.subscribe('cache:invalidate')

        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                book_id = message['data'].decode('utf-8')
                await redis_util.delete(book_id)


in_invalidator = Invalidator()
