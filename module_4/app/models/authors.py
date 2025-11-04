from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Author(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    descript: Mapped[str] = mapped_column(String(100), nullable=True)
