import pytest

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from testcontainers.postgres import PostgresContainer
from module_4.app.main import app

from module_4.app.models.base import get_session
from module_4.app.models import Base, Book


@pytest.mark.asyncio
async def test_e2e_real_db_async():
    with PostgresContainer("postgres") as postgres_container:
        # Получаем URL и конвертируем для asyncpg
        original_url = postgres_container.get_connection_url()
        async_db_url = original_url.replace(
            "postgresql+psycopg2://", "postgresql+asyncpg://"
        )
        async_engine = create_async_engine(async_db_url)
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        session_maker = async_sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with session_maker() as session:
            book = Book(title="Test", year=2024)
            session.add(book)
            await session.commit()

        app.dependency_overrides[get_session] = lambda: session_maker()

        try:
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://tests"
            ) as ac:
                response = await ac.get('/books')
                assert response.status_code == 200

                response_create = await ac.post(
                    '/books/books_id',
                    json=dict(title="Test", year=2024)
                )
                assert response_create.status_code == 201
                response_get = await ac.get('/books')
                assert response_get.status_code == 200
                books = response_get.json()
                assert len(books) > 0
        finally:
            app.dependency_overrides.clear()
