from sqlalchemy import Integer, String
from sqlalchemy.orm import declared_attr, mapped_column, declarative_base

class PreBse:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = mapped_column(Integer, primary_key=True)

Base = declarative_base(cls=PreBse)