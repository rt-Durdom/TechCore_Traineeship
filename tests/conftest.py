import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.testclient import TestClient

from module_4.app.main import app

engine = create_engine("sqlite:///:memory:")
Base_QL = declarative_base()
fast_test_client = TestClient(app)

@pytest.fixture
def db_session():
    Base_QL.metadata.create_all(engine)
    LocalSession = sessionmaker(engine)
    with LocalSession() as session:
        yield session
