import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///:memory:")
Base_QL = declarative_base()

@pytest.fixture
def db_session():
    Base_QL.metadata.create_all(engine)
    LocalSession = sessionmaker(engine)
    with LocalSession() as session:
        yield session
