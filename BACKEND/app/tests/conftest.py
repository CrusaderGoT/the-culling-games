'''configuraturations for test, i.e, fixtures, dependecy overrides, etc.'''
import pytest
from sqlmodel import SQLModel, Session
from sqlalchemy import create_engine
from fastapi.testclient import TestClient

from app.tests.utils_test import (
    create_test_player, create_test_user, login_test_user,
    override_dependencies, setup_authenticated_client
    )
from ..api.main import app
from dotenv import load_dotenv
import os


@pytest.fixture(scope="session", autouse=True)
def test_env():
    'load enviroment file'
    return load_dotenv(".env.test")


@pytest.fixture(scope="session")
def test_engine():
    'create sqlalchemy/sqlmodel engine.\n the test engine'
    _test_engine = create_engine(
        os.getenv("SQLITE_DATABASE_URL", "sqlite:///./test.db"),
        connect_args={"check_same_thread": False},
    )
    return _test_engine
    

@pytest.fixture(scope="session", autouse=True)
def setup_test_database(test_engine):
    """
    Fixture to create the tables once for all tests and drop them after all tests complete.
    """
    # Create tables before running tests
    SQLModel.metadata.create_all(test_engine)
    yield
    # Drop tables after all tests have run
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="module")
def test_session(test_engine):
    """
    `create a new database session that commits at the end of the test`
    """
    with Session(test_engine) as session:
        yield session
        

@pytest.fixture(scope="module", autouse=True)
def override_app_dependencies(test_session):
    yield override_dependencies(test_session)
    app.dependency_overrides = {}

@pytest.fixture(scope="function")
def test_client():
    "create a test client that uses the test_session"
    with TestClient(app) as tst_cli:
        yield tst_cli

@pytest.fixture(scope="module")
def module_test_client():
    """
    create a test client that uses the test_session.\n
    `for module scope use`
    """
    with TestClient(app) as tst_cli:
        yield tst_cli

@pytest.fixture(scope="function")
def authenticated_test_client(test_client) -> tuple[TestClient, dict]:
    'an aunthenticated client that their session commits'
    #  use test client to create a user and then login them in to get access token
    test_user = create_test_user(test_client).json()
    token = login_test_user(test_client, test_user["id"])
    client = setup_authenticated_client(test_client, token)
    return client, test_user

@pytest.fixture(scope="function")
def authenticated_admin_client(test_client) -> tuple[TestClient, dict]:
    'an aunthenticated admin client, that commits'
    test_user = create_test_user(test_client).json()
    code = os.getenv("CODE")
    super_uer_res = test_client.post(f"/admin/superuser/{test_user['id']}", params={"code": code})
    assert super_uer_res.is_success == True
    token = login_test_user(test_client, test_user["id"])
    client = setup_authenticated_client(test_client, token)
    return client, test_user

@pytest.fixture(scope="module")
def match_players(module_test_client) -> list[tuple[TestClient, dict]]:
    """
    Create players and authenticated clients for match tests.
    Returns a list of tuples: (authenticated client, player data).
    """
    players_info = []
    for _ in range(2):
        # Create a new test user
        test_user = create_test_user(module_test_client)
        assert test_user.is_success == True
        token = login_test_user(module_test_client, test_user.json()["id"])
        assert token

        # Create a new authenticated client for this user
        auth_client = TestClient(app)
        auth_client.headers.update({"Authorization": f"Bearer {token}"})

        # Create a player for the user
        player_res = create_test_player((auth_client, test_user.json()))
        assert player_res.is_success
        player_data = player_res.json()

        # Append client and player info to the list
        players_info.append((auth_client, player_data))

    return players_info
