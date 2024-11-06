'''
test file for the users routers/paths
'''
from typing import Literal
from fastapi.testclient import TestClient
from ..models.user import CreateUser, EditUser, UserInfo, Country
from fastapi.encoders import jsonable_encoder as je
from datetime import date


user_info_keys = UserInfo.model_fields.keys() # expected keys
'expected return keys, for the user route/ userinfo'

def test_create_user(test_client: TestClient):
    'test for the creation of a user'
    create_user_payload = CreateUser(
    username="test_username",
    email="testuser@example.com",
    country=Country("NG"),
    password="Crusader45@",
    confirm_password="Crusader45@"
    )
    response = test_client.post("/signup", json=je(create_user_payload))
    # check status is created
    assert response.status_code == 201
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] is not None and type(response.json()["id"]) is int
    assert response.json()["created"] == str(date.today())
    # check userpayload values match the response user
    for k in create_user_payload.model_dump().keys():
        if k in res_keys:
            assert response.json()[k] == create_user_payload.model_dump()[k]


def test_current_user(autheticated_test_client: TestClient):
    'test get the current user'
    response = autheticated_test_client.get("/users/me")
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

def test_a_user(autheticated_test_client: TestClient, user_id: Literal[1]):
    'test for getting a specific user'
    response = autheticated_test_client.get(f"/users/{user_id}")
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] == user_id and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check if response values match setup user values
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_edit_user(autheticated_commiter_client: TestClient, user_id: Literal[1]):
    'test for edit user'
    edit_user_payload = EditUser(
        username="editedtestuser",
        email="editedmail@example.com",
        country=Country("JP")
    )
    response = autheticated_commiter_client.patch(f"/users/edit/{user_id}", json=je(edit_user_payload))
    # check status is successful
    assert response.is_success == True
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields was made
    assert response.json()["id"] == user_id and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check userpayload values match the response user
    for k in edit_user_payload.model_dump().keys():
        if k in res_keys:
            assert response.json()[k] == edit_user_payload.model_dump()[k]

def test_delete_user(autheticated_commiter_client: TestClient,
                    autheticated_test_client: TestClient, user_id: Literal[1]):
    response = autheticated_commiter_client.delete(f"/users/delete/1")
    # check status is successful
    print(response.json())
    assert response.is_success == False
    # check returned keys are the expected keys
    res_keys = response.json().keys() # response keys
    assert res_keys == user_info_keys
    # check database calculated fields matches
    assert response.json()["id"] == user_id and type(response.json()["id"]) is int
    assert response.json()["created"] is not None and type(response.json()["created"]) is str
    # check is user no longer exists in database
    
