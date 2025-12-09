from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime

from module_4.app.schemas.reviews import ReviewSchema, ReviewInput


class ReviewService:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.database = client.techcore_db
        self.collection = self.database.reviews

    async def create_review(self, review: ReviewSchema):
        review_data = review.model_dump()
        review_data["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(review_data)
        return ReviewInput(
            id=str(result.inserted_id),
            **review_data
        )

    async def get_for_product(self, product_id: str):
        messages = self.collection.find({"product_id": product_id})
        reviews = []

        async for item in messages:
            item_data = {
                "id": str(item["_id"]),
                "product_id": item["product_id"],
                "comment": item["comment"],
                "created_at": item["created_at"],
            }
            reviews.append(ReviewInput(**item_data))

        return reviews

    async def get_review(self, review_id: str):
        rew = await self.collection.find_one({"_id": ObjectId(review_id)})
        if rew:
            item_data = {
                "id": str(rew["_id"]),
                "product_id": rew["product_id"],
                "comment": rew["comment"],
                "created_at": rew["created_at"],
            }
            return ReviewInput(**item_data)
        return None

    async def delete_review(self, review_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(review_id)})
        return result.deleted_count > 0