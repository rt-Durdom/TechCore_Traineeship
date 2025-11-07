from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Book(Base):

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    #author_id: Mapped[int] = mapped_column(ForeignKey('author.id'), nullable=True)

    #relationships
    #author: Mapped['Author'] = relationship('Author', back_populates='books')