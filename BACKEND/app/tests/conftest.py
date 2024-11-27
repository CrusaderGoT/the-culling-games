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


# load enviroment file
load_dotenv()

# SQLITE Database for testing
SQLITE_DATABASE_URL = "sqlite:///./test.db"
'the test database url'

# create sqlalchemy/sqlmodel engine
test_engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    )
'the test engine'

@pytest.fixture(scope="session")
def setup_test_database():
    """
    Fixture to create the tables once for all tests and drop them after all tests complete.
    """
    # Create tables before running tests
    SQLModel.metadata.create_all(test_engine)
    yield
    # Drop tables after all tests have run
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def test_session(setup_test_database, setup_match_players):
    """
    `create a new database session that commits at the end of the test`
    """
    with Session(test_engine) as session:
        yield session

@pytest.fixture(scope="function")
def test_client(test_session):
    "create a test client that uses the test_session_commiter"
    override_dependencies(test_session)
    with TestClient(app) as tst_cli:
        yield tst_cli
        app.dependency_overrides = {}

@pytest.fixture(scope="function")
def authenticated_test_client(test_client) -> tuple[TestClient, dict]:
    'an aunthenticated client that their session commits'
    #  use test client to create a user and then login them in to get access token
    test_user = create_test_user(test_client)
    token = login_test_user(test_client, test_user["id"])
    client = setup_authenticated_client(test_client, token)
    return client, test_user

@pytest.fixture(scope="function")
def authenticated_admin_client(test_client) -> tuple[TestClient, dict]:
    'an aunthenticated admin client, that commits'
    test_user = create_test_user(test_client)
    code = os.getenv("CODE")
    super_uer_res = test_client.post(f"/admin/superuser/{test_user['id']}", params={"code": code})
    assert super_uer_res.is_success == True
    token = login_test_user(test_client, test_user["id"])
    client = setup_authenticated_client(test_client, token)
    return client, test_user

@pytest.fixture(scope="function")
def setup_match_players() -> list[tuple[TestClient, dict]]:
    """
    Create players and authenticated clients for match tests.
    Returns a list of tuples: (authenticated client, player data).
    """
    client = TestClient(app)
    players_info = []
    for _ in range(2):
        # Create a new test user
        test_user = create_test_user(client)
        login_res = client.post("/login", data={
            "username": test_user["id"],
            "password": "Password",
        })
        assert login_res.status_code == 200
        token = login_res.json().get("access_token")
        assert token

        # Create a new authenticated client for this user
        ac = TestClient(app)
        ac.headers.update({"Authorization": f"Bearer {token}"})

        # Create a player for the user
        player_res = create_test_player((ac, test_user))
        assert player_res.is_success
        player_data = player_res.json()

        # Append client and player info to the list
        players_info.append((ac, player_data))

    return players_info