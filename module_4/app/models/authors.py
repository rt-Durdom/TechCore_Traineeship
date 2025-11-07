from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Author(Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    descript: Mapped[str] = mapped_column(String(100), nullable=True)

    #relationship
    #books: Mapped[list['Book']] = relationship('Book', back_populates='author')
