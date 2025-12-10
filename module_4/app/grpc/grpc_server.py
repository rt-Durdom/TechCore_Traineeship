import asyncio
import grpc
from module_4.app.models.async_crud import CRUDAsyncBase
from module_4.app.models.books import Book
from module_4.app.models.base import local_async_session

from module_4.app.grpc import book_pb2, book_pb2_grpc


class BookServiceServicer(book_pb2_grpc.BookServiceServicer):

    async def GetBook(self, request, context):
        async with local_async_session() as session:
            db_obj = await CRUDAsyncBase(Book).retrive(request.id, session)

            return book_pb2.GetBookResponse(
                book=book_pb2.Book(
                    id=db_obj.id,
                    title=db_obj.title,
                    year=db_obj.year or 0
                )
            )


async def serve():
    server = grpc.aio.server()

    book_pb2_grpc.add_BookServiceServicer_to_server(
        BookServiceServicer(), server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Стартуем на порте 50051")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
