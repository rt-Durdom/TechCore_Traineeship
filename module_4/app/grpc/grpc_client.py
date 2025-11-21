import asyncio
import grpc
from app.grpc import book_pb2, book_pb2_grpc


async def run():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = book_pb2_grpc.BookServiceStub(channel)

        response = await stub.GetBook(
            book_pb2.GetBookRequest(id=1)
        )

        print('Книга:', response.book)


if __name__ == "__main__":
    asyncio.run(run())
