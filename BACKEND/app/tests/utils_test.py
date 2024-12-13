from datetime import timedelta
from random import choice, sample

from sqlmodel import SQLModel, Session, func, select

from app.api.main import app
from app.models.base import ActionTimePoint
from app.models.colony import Colony
from app.models.player import CreateCT, CreateCTApp, CreatePlayer, Player
from app.models.user import Country, CreateUser

from fastapi.encoders import jsonable_encoder as je
from fastapi.testclient import TestClient

from app.utils.dependencies import get_or_create_colony, get_session


# UTILS
def gen_rand_username():
    alphas = [*"a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0 _".split(' ')]
    username = "".join(sample(alphas, k=20))
    return username


def gen_rand_email():
    alphas = [*"a b c d e f g h i j k l m n o p q r s t u v w x y z _".split(' ')]
    email = "".join(sample(alphas, k=8)) + "@example.com"
    return email


def player_payload():
    c_player_payload = CreatePlayer(
        name="testplayer",
        gender=CreatePlayer.Gender("male"),
        age=25,
        role="programmer"
    )
    c_ct = CreateCT(
        name="git push",
        definition="commit on friday, trust me bro"
    )
    c_ct_apps = [
        CreateCTApp(application="first"),
        CreateCTApp(application="second"),
        CreateCTApp(application="third"),
        CreateCTApp(application="fourth"),
        CreateCTApp(application="fifth"),
    ]
    player_dict = {"player": c_player_payload,
                   "cursed_technique": c_ct,
                   "applications": c_ct_apps}

    return player_dict

def user_payload():
    pyld = CreateUser(
        username = gen_rand_username(),
        email = gen_rand_email(),
        country=Country("NG"),
        password="Password",
        confirm_password="Password"
    )
    
    return pyld


def create_test_player(authenticated_test_client: tuple[TestClient, dict]):
    'creates a test player, and returns the Reponse object'
    user = authenticated_test_client[1]
    created_res = authenticated_test_client[0].post(f"/player/create/{user["id"]}", json=je(player_payload()))
    # check status is created
    assert created_res.status_code == 201
    return created_res

def create_test_user(test_client: TestClient):
    '''creates a brand new test user. returns the user info\n
    should typically be used in a function
    that uses the test_client pytest fixture as an arg.'''
    create_user_payload = user_payload()
    new_user_res = test_client.post("/signup", json=je(create_user_payload))
    # check status is created
    assert new_user_res.status_code == 201
    return new_user_res


# DEPENDENCIES

def get_or_create_colony_test(session: Session):
    '''
    returns a colony with less than 10 PLAYERS or returns a new base colony.
    `for tests`.'''
    # get a random colony to add the player
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
    
class ATPTest(SQLModel):
    'class for duration, limit, point, etc. of techniques, match, etc. `for tests`'
    match_duration: timedelta = timedelta(seconds=30)
    domain_duration: timedelta = timedelta(seconds=30)
    simple_domain_duration: timedelta = timedelta(seconds=30)

    vote_binding_vow_limit: int = 3

    limit_binding_vow: int = 5
    limit_domain_expansion: int = 5
    limit_simple_domain: int = 5

    cost_binding_vow: float = 0
    cost_domain_expansion: float = 0
    cost_simple_domain: float = 0

    vote_point: float = 0.2
    domain_expansion_point:float = 4.0
    simple_domain_point:float = 2.0



def override_dependencies(session):
    """Central function for overriding dependencies."""
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_or_create_colony] = lambda: get_or_create_colony_test(session)
    app.dependency_overrides[ActionTimePoint] = ATPTest


def login_test_user(client, username: str, password: str = "Password") -> str:
    """Helper to log in a test user and return their token."""
    response = client.post("/login", data={"username": username, "password": password})
    assert response.is_success
    return response.json().get("access_token")


def setup_authenticated_client(client: TestClient, token: str):
    """Set up a client with the given token."""
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
