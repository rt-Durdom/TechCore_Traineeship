from typing import Optional

from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    title: str = Field(..., min_length=1)
    year: Optional[int] = Field(default=None)


class BookDB(BaseModel):
    title: str = Field(..., min_length=1)
    year: Optional[int] = Field(default=None)

class BookRead(BookDB):
    id: int
