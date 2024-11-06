'''configuraturations for test, i.e, fixtures, dependecy overrides, etc.'''
import pytest
from sqlmodel import Session, SQLModel, select
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from ..api.main import app
from ..utils.dependencies import get_session, get_or_create_colony
from ..models.colony import *
from ..models.user import *
from ..models.player import *
from ..models.match import *
from ..models.admin import *
from ..auth.credentials import PasswordAuth as pw_auth
from sqlmodel import Session, select, func
from random import choice

# SQLITE Database for testing
SQLITE_DATABASE_URL = "sqlite:///./test.db"
'the test database url'

# create sqlalchemy/sqlmodel engine
test_engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    )
'the test engine'

# create tables in test database
SQLModel.metadata.create_all(test_engine)

@pytest.fixture
def user_id():
    "User Id of the `setup_user` as a Path parameter; for tests."
    return 1



def setup_user(session: Session):
    'a user that persists in the test database'
    # check if user already exists
    user = session.exec(
        select(User)
        .where(User.id == 1)
        .where(User.username == "testuser")
        ).first()
    if not user:
        # create the user only if it doesn't exist
        # hash password
        pw = pw_auth().hash_password("Password")
        user = User(
            username="testuser",
            usernamedb="testuser",
            email="test@example.com",
            password=pw,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

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
    "create a test client that uses the test_get_session"
    app.dependency_overrides[get_session] = test_get_session
    app.dependency_overrides[get_or_create_colony] = get_or_create_colony_test
    with TestClient(app) as tst_cli:
        with Session(test_engine) as session:
            setup_user(session)
        yield tst_cli
    app.dependency_overrides = {}

@pytest.fixture(scope="function")
def autheticated_test_client(test_client) -> TestClient:
    'an aunthenticated client'
    #  use test client to get the setup_user and get access token
    login_res = test_client.post("/login", data={
        "username": "testuser",
        "password": "Password",
    })
    assert login_res.is_success == True
    token = login_res.json().get("access_token")
    assert token
    # add token to test client header
    test_client.headers.update({"Authorization": f"Bearer {token}"})
    return test_client

def test_session_commiter():
    "create a new database session that commits at the end of the test"
    with Session(test_engine) as session:
        yield session

@pytest.fixture(scope="function")
def test_client_commiter():
    "create a test client that uses the test_session_commiter"
    app.dependency_overrides[get_session] = test_session_commiter
    with TestClient(app) as tst_cli:
        yield tst_cli
        app.dependency_overrides = {}

@pytest.fixture(scope="function")
def autheticated_commiter_client(test_client_commiter) -> TestClient:
    'an aunthenticated client that their session commits'
    #  use test client to get the setup_user and get access token
    login_res = test_client_commiter.post("/login", data={
        "username": "testuser",
        "password": "Password",
    })
    assert login_res.is_success == True
    token = login_res.json().get("access_token")
    assert token
    # add token to test client header
    test_client_commiter.headers.update({"Authorization": f"Bearer {token}"})
    return test_client_commiter

# for players router
def get_or_create_colony_test():
    '''returns a colony with less than 10 PLAYERS or returns a new base colony.
    `for tests`'''
    # get a random colony to add the player
    with Session(test_engine) as session:
        subquery = (
            select(Colony.id, func.count(Player.id).label("player_count"))
            .join(Player, isouter=True)
            .group_by(Colony.id)
            .having(func.count(Player.id) < 10)
        ).subquery()
        colony = session.exec(
            select(Colony).where(Colony.id.in_(select(subquery.c.id)))
        ).first()
        if colony:
            return colony
        else: # return new colony instance
            # select a random country
            countries = list(Country)
            country = choice([c for c in countries])
            colony = Colony(country=country)
            return colony