import json
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from .base import Base
from core.db import redis_util

ModelType = TypeVar('ModelType', bound=Base)


async def check_cache(id: int):
    cache_ = await redis_util.get(id)
    if cache_:
        return True
    else:
        return False


class CRUDAsyncBase:
    def __init__(self, model):
        self.model = model

    async def retrive(self, obj_id: int, session: AsyncSession):
        return (await session.execute(select(self.model).where(self.model.id == obj_id))
                .scalars().first())

    async def get(self, session: AsyncSession) -> list[ModelType]:
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
        self,
        object_in,
        session: AsyncSession,
        # commit: bool = True
    ):
        object_data = object_in.dict()
        db_object = self.model(**object_data)
        session.add(db_object)
        # if commit:
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def update(
            self,
            db_object,
            object_in,
            session: AsyncSession,
            # commit: bool = True
    ):
        obj_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])

        session.add(db_object)
        # if commit:
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(
        self,
        id: int,  # Принимаем ID вместо объекта
        session: AsyncSession,
    ):
        # Находим объект в базе
        db_obj = await session.get(self.model, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Объект не найден")
        # Удаляем объект
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    #TEXT = 'SELECT books.title, authors.name FROM books JOIN authors ON authors.id = books.author_id'

    async def get_obj_by_id(self, obj_id: int, session: AsyncSession):
        if check_cache(obj_id):
            return await json.loads(redis_util.get(obj_id))
        else:
            results = (await session.execute( #вместо select можно вставить  TEXT, но он будет только для одной модели
                select(self.model).where(self.model.id == obj_id)
                )).scalars().first()
            return await redis_util.set(obj_id, json.dumps(results))
