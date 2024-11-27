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
    "User Id of the `setup_user` as a fixture; for tests."
    return 1

@pytest.fixture
def player_id():
    "Player Id of the player created during test as a fixture. If client error (4xx), then likely there are multiple players in DB"
    return 1

def setup_user(session: Session):
    'a user that is committed in the test database; of the ID 1'
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
            country=Country("JP"),
            password=pw,
        )
        session.add(user)
        session.commit()

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
            # used with a new session instance since we want the setup user
            # to persist in the DB
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
        with Session(test_engine) as session:
            # set up user for persistent use
            setup_user(session)
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


def match_player():
    'returns a player instance for use in setup player'
    # create 3 players for test purposes
    c_player_payload = CreatePlayer(
        name="testplayer",
        gender=CreatePlayer.Gender("male"),
        age=25,
        role="programmer"
    )
    c_ct_apps = [
        CTApp(application="first", number=1),
        CTApp(application="second", number=2),
        CTApp(application="third", number=3),
        CTApp(application="fourth", number=4),
        CTApp(application="fifth", number=5),
    ]
    c_ct = CursedTechnique(
        name="git push",
        definition="commit on friday, trust me bro",
        applications=c_ct_apps
    )
    player = Player(**c_player_payload.model_dump(), cursed_technique=c_ct)
    return player

def setup_match_players(session: Session):
    'players to use during test, 3 in number'
    for i in range(3):
        exist_session_player = session.get(Player, i)
        if not exist_session_player:
            session_player = match_player()
            #session_player.colony = get_or_create_colony_test()
            session.add(session_player)
    # commit after the loop so all the player are available after
    # commit during the loop won't save the player since the preferred session will rollback
    session.commit()