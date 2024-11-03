'''configuraturations for test, i.e, fixtures, dependecy overrides, etc.'''
import pytest
from sqlmodel import Session, SQLModel
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from ..api.main import app
from ..utils.dependencies import get_session
from ..models.colony import *
from ..models.user import *
from ..models.player import *
from ..models.match import *
from ..models.admin import *


# SQLITE Database for testing
SQLITE_DATABASE_URL = "sqlite:///./test.db"

# create sqlalchemy/sqlmodel engine
test_engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True)

# create tables in test database
SQLModel.metadata.create_all(test_engine)

def test_get_session():
    "create a new database session with a rollback at the end of the test"
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def test_client():
    "create a test client that uses the override_get_db fixture"
    app.dependency_overrides[get_session] = test_get_session
    with TestClient(app) as tst_cli:
        yield tst_cli
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def autheticated_test_client():
    ''
