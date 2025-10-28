from typing import Optional

from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    year: Optional[int] = Field(default=None)
