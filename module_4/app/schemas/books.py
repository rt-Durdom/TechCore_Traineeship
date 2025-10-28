from typing import Optional

from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    year: Optional[int] = None
