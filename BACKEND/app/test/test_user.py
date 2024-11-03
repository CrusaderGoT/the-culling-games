'''
test file for the users routers/paths
'''
from fastapi.testclient import TestClient
from ..models.user import CreateUser, UserInfo, Country
from fastapi.encoders import jsonable_encoder as je
from datetime import date
from random import choice


user_info_keys = UserInfo.model_fields.keys() # expected keys
'expected return keys, for the user info'

user_path = choice(["testuser", 1, "test@example.com"])
"Auto random user Id, Username, or Email of the setup_user as a Path parameter; for tests."

def test_create_user(test_client: TestClient):
    'test for the creation of a user'
    user_payload = CreateUser(
    username="test_username",
    email="testuser@example.com",
    country=Country("NG"),
    password="Crusader45@",
    confirm_password="Crusader45@"
    )
    response = test_client.post("/signup", json=je(user_payload))
    # check status is created
    assert response.status_code == 201
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] is not None and type(response.json()["id"]) is int
    assert response.json()["created"] == str(date.today())
    # check userpayload values match the response user
    for k in user_payload.model_dump().keys():
        if k in res_keys:
            assert response.json()[k] == user_payload.model_dump()[k]


def test_current_user(autheticated_test_client: TestClient):
    'test get the current user'
    response = autheticated_test_client.get("users/me")
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] is not None and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check if response values match setup user values
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_a_user(autheticated_test_client: TestClient):
    'test for getting a specific user'
    response = autheticated_test_client.get(f"users/{user_path}")
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] is not None and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check if response values match setup user values
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"