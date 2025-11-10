from typing import Optional
from datetime import datetime

from pydantic import BaseModel



class ReviewSchema(BaseModel):
    product_id: str
    comment: str


class ReviewInput(BaseModel):
    id: str
    product_id: int
    comment: str
    created_at: datetime
    #author_id: Optional[int] = None

    class Config:
        from_attributes = True
