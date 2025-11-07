from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson.errors import InvalidId

from app.crud.mongo_crud import ReviewService
from app.schemas.reviews import ReviewSchema, ReviewInput
from app.core.db import get_review_service

router = APIRouter()


@router.post("/api/reviews", response_model=ReviewInput)
async def create_review(
    review: ReviewSchema, 
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.create_review(review)


@router.get("/api/products/{product_id}/reviews", response_model=List[ReviewInput])
async def get_product_reviews(
    product_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    return await review_service.get_reviews_id(product_id)


@router.get("/api/reviews/{review_id}", response_model=ReviewInput)
async def get_review(
    review_id: str,
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
    review_id: str,
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
