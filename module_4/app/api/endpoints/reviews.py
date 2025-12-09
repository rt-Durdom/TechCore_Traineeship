import asyncio
from typing import List
from bson.errors import InvalidId

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from module_4.app.crud.mongo_crud import ReviewService
from module_4.app.schemas.reviews import ReviewSchema, ReviewInput
from module_4.app.core.db import get_review_service
from module_4.app.models.base import get_session
from module_4.app.models.async_crud import CRUDAsyncBase
from module_4.app.models.books import Book

router = APIRouter()


@router.post("/api/reviews", response_model=ReviewInput)
async def create_review(
    review: ReviewSchema, 
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.create_review(review)


@router.get("/api/products/{product_id}/details")
async def get_product_reviews(
    product_id: int,
    review_service: ReviewService = Depends(get_review_service),
    session: AsyncSession = Depends(get_session)
):
    book_task = CRUDAsyncBase(Book).get_obj_by_id(product_id, session)
    reviews_task = review_service.get_for_product(product_id)
    book,reviews = await asyncio.gather(book_task, reviews_task)
    return f'Букс: {book}, Отзывс: {reviews}'


@router.get("/api/reviews/{review_id}", response_model=ReviewInput)
async def get_review(
    review_id: int,
    review_service: ReviewService = Depends(get_review_service)
):
    try:
        review = await review_service.get_review(review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нету такого отзыва"
            )
        return review
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильно задан ID отзыва"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Какая-то ошибка: {str(e)}"
        )


@router.delete("/api/reviews/{review_id}")
async def delete_review(
    review_id: int,
    review_service: ReviewService = Depends(get_review_service)
):
    try:
        success = await review_service.delete_review(review_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нету такого отзыва"
            )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильно задан ID отзыва"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Какая-то ошибка: {str(e)}"
        )
